# Davis--Kahan sin Theta 定理（1970）：特征子空间扰动的精确度量

## 作者

Chandler Davis & W. M. Kahan

## 发表时间与刊物

1970 年，发表于 *SIAM Journal on Numerical Analysis*，第 7 卷第 1 期，第 1--46 页。论文题为 "The Rotation of Eigenvectors by a Perturbation. III"。这是 Davis 关于特征向量扰动系列研究的第三篇（也是最具影响力的一篇），前两篇分别发表于 1963 年和 1965 年的 *Journal of Mathematical Analysis and Applications*。该论文是 SIAM Journal on Numerical Analysis 历史上被引用最多的论文之一，至今累积引用已超过一千六百次。

## 一句话概括

对于 Hermite 矩阵在扰动下其特征子空间发生的"旋转"，该定理给出了以扰动矩阵范数与特征值间距之比为上界的最优估计，从而将矩阵扰动理论从特征值层面推进到了特征子空间层面。

---

## 1. 历史背景

二十世纪五六十年代是数值线性代数从"经验技艺"蜕变为"严格科学"的关键时期。电子计算机的迅速普及使得大规模矩阵计算成为可能，但也暴露出浮点运算中舍入误差对计算结果的深刻影响。在这一背景下，矩阵扰动理论——研究矩阵微小变化如何影响其谱性质的数学分支——逐渐成为数值分析的核心课题之一。

特征值扰动理论的历史可以追溯到更早的时期。1912 年，Hermann Weyl 证明了 Hermite 矩阵特征值在扰动下的稳定性不等式：若 $A$ 和 $\tilde{A} = A + E$ 均为 $n$ 阶 Hermite 矩阵，则特征值的变化满足 $\max_i |\lambda_i(A) - \lambda_i(\tilde{A})| \le \|E\|$。这一不等式的证明依赖于 Courant--Fischer 极小极大原理，揭示了特征值映射的 Lipschitz 连续性。1953 年，Hoffman 与 Wielandt 将这一估计推广到了 Frobenius 范数下的整体控制，证明了特征值差的平方和可以被扰动矩阵的 Frobenius 范数的平方所控制。这些结果构成了所谓"特征值扰动理论"的经典框架，为数值计算中特征值算法的误差分析提供了坚实的理论基础。

然而，一个自然且根本性的问题始终悬而未决：特征值的稳定性并不自动意味着特征向量（或更准确地说，特征子空间）的稳定性。当两个特征值非常接近时，对应的特征向量可能因为微小的扰动而发生剧烈的旋转——这在数值计算中是极为常见且棘手的现象。在量子力学中，Hamiltonians 的特征子空间（即能量本征态张成的空间）的稳定性直接关系到物理系统的可观测性质。在统计学中，主成分分析依赖于协方差矩阵特征向量的估计。在所有这些场景中，仅仅知道特征值是稳定的远远不够。

Chandler Davis（1926--2022）是一位兼具数学深度与人文关怀的学者。他于 1942 年进入 Harvard 学习，1950 年在 Garrett Birkhoff 指导下获得博士学位，研究方向是算子理论。1953 年，他因拒绝在众议院非美活动委员会（HUAC）面前交代政治信仰而被 University of Michigan 解聘，1959 年入狱六个月。出狱后，在几何学家 Coxeter 的帮助下来到 University of Toronto，在那里度过了三十余年的学术生涯，专注于算子理论和线性代数，指导了十五名博士生。2012 年成为 American Mathematical Society Fellow，2022 年辞世。

Davis 从 1963 年开始发表"特征向量旋转"系列论文。第一篇（1963）独立发表在 *Journal of Mathematical Analysis and Applications* 上，首次提出了衡量特征向量偏移的基本框架，给出了算子范数下的初步估计，开创性地将"旋转"这一几何概念引入扰动分析。第二篇（1965）在同一期刊上发表，做了进一步的技术改进。但这两篇论文的结果局限于算子范数（即谱范数），且证明工具相对初等。

William Morton Kahan（1933 年生于加拿大）则是另一位传奇人物。他在 University of Toronto 完成了从本科到博士的全部训练（1958 年获博士学位），研究方向是数值分析。1968 年，Kahan 离开 Toronto 前往 University of California, Berkeley，加入新成立的计算机科学系。在 Berkeley，他与 Gene Golub 合作提出的 Golub--Kahan bidiagonalization 成为奇异值分解的核心算法之一。1980 年代，他主持设计了 IEEE 754 浮点运算标准——这一标准至今仍是全世界几乎所有计算机处理浮点数的基础——并因"对数值分析的根本性贡献"获得 1989 年 Turing 奖。

Davis 和 Kahan 的合作可以追溯到他们在 Toronto 的交集——两人在五十年代末至六十年代末有近十年的共事时光。Davis 关注算子理论的抽象结构与几何直觉，Kahan 则精于数值计算的误差分析与定量估计——两者的结合催生了 1970 年这篇长达 46 页的鸿篇巨制。Stewart 和 Sun 在其 1990 年的经典教材中评价这篇论文时写道，其"内容之深刻足以为其晦涩辩护"（"its content more than justifies its impenetrability"）。与前两篇论文相比，第三篇的核心突破在于两个方面：一是将估计从算子范数推广到了任意酉不变范数（unitarily invariant norms），大幅扩展了定理的适用范围；二是引入了"典范角"（canonical angles）这一优雅的几何语言来统一描述子空间之间的距离，使得定理的陈述和证明具有了深刻的几何意蕴。

---

## 2. 核心问题

设 $A$ 为 $n$ 阶 Hermite 矩阵，$\tilde{A} = A + E$ 为其扰动，其中 $E$ 也是 Hermite 矩阵。设 $A$ 的某一组特征值 $\{\lambda_1, \dots, \lambda_r\}$ 构成一个"簇"（cluster），对应的特征子空间为 $\mathcal{V}$；$\tilde{A}$ 的对应特征子空间为 $\tilde{\mathcal{V}}$。

核心问题是：$\mathcal{V}$ 与 $\tilde{\mathcal{V}}$ 之间的"距离"有多大？这个距离能否用扰动 $E$ 的大小以及特征值簇与其余特征值之间的间距（spectral gap）来定量估计？

这个问题之所以深刻，在于它触及了"特征值"与"特征向量"之间根本性的不对称。Weyl 不等式告诉我们特征值本身是稳定的——更精确地说，特征值映射是 Lipschitz 连续的。但特征向量的情况远为复杂。考虑一个简单的 $2 \times 2$ 例子：若 $A = \text{diag}(\lambda, \lambda + \varepsilon)$，其中 $\varepsilon$ 极小，则一个很小的非对角扰动 $E$ 就可能使两个特征向量几乎交换方向——特征值几乎不变，但特征向量发生了接近 $90°$ 的旋转。更极端地，当 $\varepsilon = 0$（即特征值重合）时，特征空间是二维的，其中任何一个方向都是特征向量，"特征向量"的概念本身变得不确定。

Davis 和 Kahan 的关键洞察是：不应该试图控制单个特征向量的变化，而应该考察整个特征子空间的旋转。即使单个特征向量可以在特征子空间内部自由旋转（当存在重特征值时），子空间本身作为一个整体却具有良好的连续性。这一从"向量"到"子空间"的概念飞跃，为扰动理论开辟了全新的道路。

Davis--Kahan 定理正是要给出这种子空间旋转角度的定量上界：旋转的角度正比于扰动的大小 $\|E\|$，反比于特征值间距 $\delta$。

---

## 3. 主要定理与结果

### 3.1 典范角（Canonical Angles / Principal Angles）

在陈述定理之前，首先需要引入衡量两个子空间之间"距离"的数学工具——典范角。

设 $\mathcal{V}$ 和 $\tilde{\mathcal{V}}$ 是 $\mathbb{C}^n$ 中两个 $r$ 维子空间。设 $V$ 和 $\tilde{V}$ 分别是它们的标准正交基矩阵（$n \times r$）。对 $V^*\tilde{V}$ 做奇异值分解，得到奇异值 $\sigma_1 \ge \sigma_2 \ge \cdots \ge \sigma_r$，其中每个奇异值不超过 1。定义典范角 $\theta_i = \arccos(\sigma_i)$，则 $0 \le \theta_1 \le \theta_2 \le \cdots \le \theta_r \le \pi/2$。这些角 $\theta_1, \dots, \theta_r$ 即为两个子空间之间的典范角（也称主角）。这一概念最早由法国数学家 Camille Jordan 在 1875 年引入，可以看作是两个向量之间的夹角向子空间的自然推广。

直观地说，$\theta_1$ 是第一个子空间中的某个方向到第二个子空间的最小角度，$\theta_2$ 是在与第一对方向正交的子空间中的最小角度，依此类推。当所有典范角为零时，两个子空间完全重合；当某个典范角为 $\pi/2$ 时，两个子空间在某个方向上完全正交。

定义对角矩阵 $\Theta = \text{diag}(\theta_1, \dots, \theta_r)$。则 $\sin\Theta$、$\cos\Theta$、$\tan\Theta$ 均为对角矩阵，其对角元素分别是各典范角的正弦、余弦和正切值。对于任意酉不变范数 $\|\cdot\|$，$\|\sin\Theta\|$ 提供了两个子空间之间距离的一种度量，且与谱投影之间有如下等价关系：$\|\sin\Theta(\mathcal{V}, \tilde{\mathcal{V}})\| = \|P_{\mathcal{V}} - P_{\tilde{\mathcal{V}}}\|$（当取算子范数时）。

### 3.2 sin Theta 定理

**定理（Davis--Kahan sin Theta）。** 设 $A$ 为 Hermite 矩阵，$\tilde{A} = A + E$。设 $A$ 的特征值分为两组：一组特征值落在区间 $[a, b]$ 内，对应特征子空间 $\mathcal{V}$；$\tilde{A}$ 的相应特征子空间为 $\tilde{\mathcal{V}}$。设

$$\delta = \min_{\lambda \in [a,b],\, \mu \notin [a,b]} |\lambda_i(A) - \lambda_j(\tilde{A})| > 0$$

即目标特征值簇与其余特征值之间的间距。则对任意酉不变范数 $\|\cdot\|_{\text{ui}}$，

$$\|\sin\Theta(\mathcal{V}, \tilde{\mathcal{V}})\|_{\text{ui}} \le \frac{\|E\|_{\text{ui}}}{\delta}$$

特别地，取算子范数（谱范数）时，有

$$\|\sin\Theta(\mathcal{V}, \tilde{\mathcal{V}})\|_2 \le \frac{\|E\|_2}{\delta}$$

取 Frobenius 范数时，有

$$\|\sin\Theta(\mathcal{V}, \tilde{\mathcal{V}})\|_F \le \frac{\|E\|_F}{\delta}$$

这一结果的优美之处在于其简洁性和普适性。上界仅涉及两个量：扰动的大小 $\|E\|$ 和谱间距 $\delta$，且对所有酉不变范数同时成立。由 Weyl 不等式可知，当 $\|E\|_2 < \delta/2$ 时，扰动不会使特征值跨越间距，从而定理的前提条件自动满足。

### 3.3 变体：tan Theta 和 sin 2Theta

原论文中还证明了两个重要变体，它们在不同条件下提供更为精细的估计：

- **tan Theta 定理**：在更强的间距条件下（要求 $A$ 的目标特征值与 $A$ 的其余特征值之间有间距，而非 $A$ 与 $\tilde{A}$ 之间），可以用 $\tan\Theta$ 替代 $\sin\Theta$。由于 $\tan\theta \ge \sin\theta$ 恒成立，tan Theta 定理的上界实际上控制了一个更大的量，因此需要更强的条件。但当扰动很小时（典范角接近零），$\tan\theta \approx \sin\theta \approx \theta$，两个估计几乎等价。tan Theta 定理在某些数值算法的收敛性分析中更为方便。

- **sin 2Theta 定理**：给出 $\|\sin 2\Theta\|$ 的上界，其分母中的间距条件更为宽松——只要求 $A$ 的目标特征值与 $A$ 自身其余特征值之间有间距。由于 $\sin 2\theta = 2\sin\theta\cos\theta \le 2\sin\theta$，sin 2Theta 定理虽然控制的量看似较小，但它的间距条件完全由原始矩阵 $A$ 决定，不涉及扰动后矩阵 $\tilde{A}$ 的特征值，因此在某些实际问题中更易于验证和使用。

这三个定理分别适用于不同的精度需求和间距条件，构成了一个完整的估计体系。在统计应用中，Yu--Wang--Samworth（2015）特别强调了 sin Theta 定理中仅使用总体特征值间距的变体的重要性，因为样本特征值的间距本身是随机的、难以控制的。

---

## 4. 核心方法

Davis 和 Kahan 的证明方法融合了几何直觉与算子代数技巧，其方法论本身对后续研究产生了深远影响。主要包括以下几个关键要素：

**典范角的几何框架。** 两个子空间之间的"距离"通过典范角来刻画。这些角是子空间之间"最直接的旋转"所需转过的角度序列。这一概念最早可以追溯到 Camille Jordan（1875），但在此后近一个世纪中主要停留在纯几何的讨论层面。Davis 和 Kahan 首次将其系统地用于扰动分析，证明了典范角与谱投影差的各种范数之间的精确等价关系。这一框架为子空间扰动问题提供了一种统一的、与坐标选取无关的描述语言。

**Sylvester 方程与分块分析。** 将 $\mathbb{C}^n$ 沿 $A$ 的不变子空间分解为直和 $\mathcal{V} \oplus \mathcal{V}^\perp$。在这一分块下，$A$ 呈对角形 $A = \text{diag}(A_1, A_2)$，而扰动 $E$ 具有非对角块。子空间 $\tilde{\mathcal{V}}$ 相对于 $\mathcal{V}$ 的偏转可以用一个算子 $X: \mathcal{V} \to \mathcal{V}^\perp$ 来刻画（$\tilde{\mathcal{V}}$ 是 $X$ 图形的列空间），而 $X$ 满足一个 Sylvester 型算子方程 $A_2 X - X A_1 = R$，其中 $R$ 与扰动 $E$ 有关。这个方程的可解性和解的范数恰好取决于 $A_1$ 和 $A_2$ 的谱的分离程度——即间距 $\delta$。当 $\delta > 0$ 时，Sylvester 算子 $T(X) = A_2 X - X A_1$ 是可逆的，其逆的范数为 $1/\delta$，从而 $\|X\| \le \|R\|/\delta$。

**谱投影与正切函数的算子不等式。** 论文的一个关键技术洞察是：子空间之间的旋转可以分解为一系列"沿典范方向"的平面旋转，每个平面旋转的角度就是对应的典范角。更重要的是，上述算子 $X$ 的奇异值恰好是各典范角的正切值 $\tan\theta_i$。因此，对 $X$ 的范数估计直接转化为对 $\|\tan\Theta\|$ 的估计。最终的 sin Theta 定理则通过 $\sin\theta \le \tan\theta$ 的三角不等式得到。

**酉不变范数的推广。** 与前两篇论文仅给出算子范数下的估计不同，第三篇论文的一大突破是将所有结果推广到了任意酉不变范数。所谓酉不变范数，是指满足 $\|UAV\| = \|A\|$ 对一切酉矩阵 $U$、$V$ 成立的矩阵范数，包括算子范数、Frobenius 范数、核范数以及所有 Schatten $p$-范数。这一推广依赖于 von Neumann 关于对称规范函数（symmetric gauge function）的表示理论以及 Ky Fan 的支配不等式。从技术上看，酉不变范数推广的关键在于证明 Sylvester 算子的逆在所有酉不变范数下都具有一致的范数界 $1/\delta$。

**残差形式。** 除了扰动形式（已知 $E$ 的范数）外，论文还给出了基于残差（residual）的估计。设 $\tilde{V}$ 是 $\tilde{\mathcal{V}}$ 的标准正交基，残差定义为 $R = A\tilde{V} - \tilde{V}({\tilde{V}}^*A\tilde{V})$。定理表明 $\|\sin\Theta\| \le \|R\|/\delta$。这一形式在数值分析中尤为实用，因为残差可以在计算过程中直接获得，而扰动 $E$ 的范数往往是未知的。

---

## 5. 重要性与影响

Davis--Kahan sin Theta 定理的问世，标志着矩阵扰动理论实现了从"特征值层面"到"特征子空间层面"的质的飞跃。此前，Weyl 不等式和 Hoffman--Wielandt 不等式虽然精确地控制了特征值的变化，但对于特征向量——这一在实际应用中往往更为重要的对象——却无能为力。Davis 和 Kahan 第一次给出了定量的、可操作的特征子空间扰动估计，且这一估计对所有酉不变范数同时成立，具有极大的普适性。

这一定理的影响远超数值分析本身，深刻地渗透到了现代科学的多个分支。在**统计学**中，主成分分析（PCA）的核心操作是提取样本协方差矩阵的前几个特征向量，用以估计数据的主要变异方向。Davis--Kahan 定理直接给出了样本特征向量与总体特征向量之间偏差的理论保证，是分析 PCA 一致性和收敛速率的标准工具。事实上，几乎所有关于高维 PCA 的现代统计理论论文都会引用这一定理。

在**机器学习**中，谱聚类（spectral clustering）的正确性分析本质上就是在估计图 Laplacian 矩阵特征子空间的扰动。Davis--Kahan 定理将聚类误差与谱间距直接联系起来，提供了谱方法性能保证的数学基础。类似地，在推荐系统和协同过滤中广泛使用的矩阵补全算法，其理论分析也离不开子空间扰动界。

在**信号处理**中，MUSIC（Multiple Signal Classification）算法和 ESPRIT 算法通过估计噪声子空间或信号子空间来确定信号源方向，其性能分析的核心步骤正是应用 Davis--Kahan 类型的扰动界来控制估计误差。

该论文的引用次数已超过 1600 次（如果算上间接引用其后续衍生结果的文献，这一数字还要大得多），是 SIAM Journal on Numerical Analysis 创刊以来被引用最多的论文之一，堪称矩阵分析领域的里程碑之作。

---

## 6. 解决了什么瓶颈

在 Davis--Kahan 定理出现之前，矩阵扰动理论面临一个根本性的"不对称"：特征值的扰动已经被 Weyl（1912）、Hoffman--Wielandt（1953）、Lidskii（1950）等人精确控制，但特征向量的扰动却缺乏可比拟的定量工具。

这个缺失并非因为问题不重要，而是因为它本质上更困难。特征值是矩阵的连续函数（甚至是 Lipschitz 连续的），但单个特征向量在特征值交叉点附近是不连续的——一个典型的例子是，当两个特征值重合时，对应的二维特征空间中任意向量都是特征向量，单个特征向量的选取不具有唯一性。更进一步，即使在特征值不重合的情况下，特征向量也只在"模去相位因子"的意义下唯一（对于实矩阵则是模去正负号）。这意味着，不能简单地用 $\|v - \tilde{v}\|$ 来衡量两个特征向量的差异，因为 $v$ 和 $-v$ 代表同一个特征方向。

Davis 和 Kahan 的关键洞察是：应该放弃对单个特征向量的追踪，转而考察整个特征子空间的旋转。子空间作为 Grassmann 流形（Grassmannian）上的点，具有良好的拓扑和微分结构。在 Grassmann 流形上，距离可以自然地通过典范角来度量，而子空间的变化则对应于 Grassmann 流形上的曲线。这一视角不仅回避了特征向量相位不确定性带来的技术困难，更揭示了扰动问题的内在几何本质。

从应用的角度看，在大多数实际场景中，人们关心的也确实是子空间而非单个向量。PCA 的前 $k$ 个主成分构成的子空间决定了最佳 $k$ 维线性投影；谱聚类中前 $k$ 个特征向量张成的子空间编码了图的社区结构；在信号处理中，信号子空间和噪声子空间的分离是 MUSIC 和 ESPRIT 等算法的基础。Davis--Kahan 定理精确地回应了这些需求。

这一思想转变——从"特征向量"到"特征子空间"——不仅解决了技术困难，更深刻地改变了人们对扰动问题的理解方式，开创了以 Grassmann 流形为舞台的子空间扰动理论。

---

## 7. 与前人工作的关系

Davis--Kahan 定理并非凭空而来，而是站在了若干重要先驱的肩膀上。理解这些学术脉络有助于把握定理的思想来源和历史定位。

**Tosio Kato 的扰动理论（1966）。** 日本数学家 Kato（1917--1999）在其经典著作 *Perturbation Theory for Linear Operators*（Springer, 1966）中系统建立了无穷维 Hilbert 空间上的算子扰动理论框架。该书涵盖了解析扰动理论、特征值的分支行为、谱投影的解析性等深刻话题，是二十世纪数学物理领域最重要的著作之一。Kato 引入的谱投影方法——通过 Cauchy 积分公式构造与指定特征值簇对应的投影算子——为 Davis--Kahan 的有限维工作提供了概念基础。Kato 的框架更为一般（适用于无穷维空间中的无界算子），但他的结果主要是定性的（存在性和连续性），而 Davis--Kahan 定理可以看作是 Kato 一般理论在有限维、定量方向上的精确化。

**Weyl 特征值不等式（1912）。** Weyl 的结果是整个扰动理论的基石。它不仅保证了特征值映射的 Lipschitz 连续性，更重要的是，它为 Davis--Kahan 定理提供了关键的前置条件。Davis--Kahan 定理中的间距 $\delta$ 之所以可以用来控制子空间旋转，根本原因在于 Weyl 不等式确保了扰动不会使特征值跳出其所在的"簇"——只要扰动 $\|E\|$ 小于间距的一半。没有 Weyl 不等式，特征值簇的稳定性就无法保证，Davis--Kahan 定理的前提条件就难以验证。

**Hoffman--Wielandt 不等式（1953）。** 此不等式提供了特征值在 Frobenius 范数意义下的整体估计：$\sum_i |\lambda_i(A) - \lambda_i(\tilde{A})|^2 \le \|E\|_F^2$。它是 Davis--Kahan 定理在 Frobenius 范数下结论的特征值层面的先驱，并且其证明中使用的最优匹配（optimal matching）技巧为后续的子空间扰动理论提供了启发。

**Jordan 的典范角（1875）。** 法国数学家 Camille Jordan 最早在欧氏空间中定义了两个子空间之间的主角（principal angles）。这一概念在提出后的近百年间主要作为一个几何观测存在，缺乏系统的应用。Davis 和 Kahan 重新发现了这一概念的威力，将其与算子范数理论和谱投影方法相结合，使之成为扰动分析的核心工具。可以说，Davis--Kahan 定理赋予了 Jordan 典范角以新的生命。

**Wilkinson 的数值分析贡献（1960 年代）。** J. H. Wilkinson 在其著作 *The Algebraic Eigenvalue Problem*（1965）中系统讨论了特征值问题的数值方法和误差分析。虽然 Wilkinson 主要关注特征值而非特征子空间，但他对向后误差分析（backward error analysis）的倡导深刻地影响了 Kahan 的学术风格。Davis--Kahan 定理的残差形式正是向后误差分析精神的体现。

---

## 8. 对后续工作的影响

Davis--Kahan 定理开创了一个丰富的研究方向，后续产生了大量重要的推广、改进和应用。

**Wedin sin Theta 定理（1972）。** 瑞典数学家 Per-Ake Wedin 在 *BIT Numerical Mathematics* 上发表了一篇具有里程碑意义的论文，将 Davis--Kahan 的结果从 Hermite 矩阵的特征子空间推广到一般（可能非方阵）矩阵的奇异子空间。具体地，设 $A$ 和 $\tilde{A} = A + E$ 为 $m \times n$ 矩阵，Wedin 定理给出了左奇异子空间和右奇异子空间在扰动下旋转角度的上界，其分母中的"间距"相应地替换为奇异值间距。这一推广使得理论可以直接应用于最小二乘问题、低秩矩阵逼近、以及一般的矩阵分解。Wedin 在论文中明确指出，他的结果"以 Davis 和 Kahan 关于 Hermite 线性算子的 sin Theta 定理为特殊情形"。

**Stewart--Sun 矩阵扰动理论（1990）。** G. W. Stewart（Johns Hopkins University）和孙继广在其专著 *Matrix Perturbation Theory*（Academic Press, 1990）中系统整理了从 Weyl 到 Davis--Kahan 到 Wedin 的全部结果，建立了现代矩阵扰动理论的标准体系。该书的第五章"不变子空间"是对 Davis--Kahan--Wedin 理论最为系统的综合，给出了统一的证明框架，讨论了各种变体的适用条件，并提供了大量计算实例。这部著作至今仍是该领域最重要的参考书。

**Bhatia 的矩阵分析（1997）。** Rajendra Bhatia 在 *Matrix Analysis*（Springer, 1997）中从更抽象的算子不等式角度重新审视了 Davis--Kahan 定理。他利用 majorization 理论和对称规范函数的性质给出了更为优雅的证明，并将结果与 von Neumann 的迹类算子理论联系起来。Bhatia 与 Davis 本人也有合作，两人共同证明了 Bhatia--Davis 不等式。

**Yu--Wang--Samworth 统计变体（2015）。** Yu、Wang 和 Samworth 在 *Biometrika* 上发表的论文"A Useful Variant of the Davis--Kahan Theorem for Statisticians"具有特殊的应用价值。他们给出了一个对统计学家更为友好的版本，具有两个关键优势：第一，间距条件仅涉及总体特征值（而非样本特征值），使得在统计推断中无需担心样本谱间距的随机波动；第二，Frobenius 范数形式的分子可以替换为算子范数乘以 $\sqrt{d}$ 和 Frobenius 范数的最小值，从而在某些高维场景中给出更紧的上界。

**Fan--Wang--Zhong 的 $\ell_\infty$ 特征向量扰动界（2018）。** 传统的 Davis--Kahan 定理在 $\ell_2$ 或 Frobenius 范数意义下控制特征子空间的偏差，但在高维统计中，逐行（entrywise, $\ell_\infty$）控制往往更为重要——例如，在社区检测中，我们需要知道每个节点的社区标签是否被正确恢复，而不仅仅是整体误差。Fan 等人的工作填补了这一空白，证明了在一定的非相干性（incoherence）条件下，特征向量的逐行扰动可以被更精细地控制。

**Cai--Zhang 的最优扰动速率（2018）。** Cai 和 Zhang 在 *Annals of Statistics* 上证明了奇异子空间扰动界的速率最优性，即 Davis--Kahan--Wedin 类型的上界在最坏情况下是不可改进的。这一结果确立了 Davis--Kahan 定理作为"最优"扰动界的地位。

---

## 9. 现代价值

进入二十一世纪，Davis--Kahan sin Theta 定理的重要性非但没有减弱，反而随着数据科学的爆发而持续攀升。以下是几个核心应用领域的详细分析。

**主成分分析（PCA）的理论保证。** 在高维统计中，PCA 是最基本的降维工具。假设数据来自均值为零、协方差矩阵为 $\Sigma$ 的分布，样本协方差矩阵 $\hat{\Sigma}$ 可以看作 $\Sigma$ 的扰动版本。Davis--Kahan 定理直接给出：样本主成分方向与总体主成分方向之间的偏差 $\|\sin\Theta(\hat{V}, V)\|$ 不超过 $\|\hat{\Sigma} - \Sigma\|/\delta$，其中 $\delta$ 是相关特征值的间距。结合随机矩阵理论对 $\|\hat{\Sigma} - \Sigma\|$ 的估计（如 $O(\sqrt{p/n})$），可以得到 PCA 一致性的非渐近保证。

**谱聚类的误差分析。** 谱聚类算法（如 Ng--Jordan--Weiss 2001 算法）的核心步骤是提取相似度矩阵（或图 Laplacian）的前 $k$ 个特征向量，然后在这些特征向量的行空间中进行 $k$-means 聚类。Davis--Kahan 定理将聚类误差与谱间距联系起来：若观测的相似度矩阵 $\hat{L}$ 是理想矩阵 $L$ 的扰动，则特征子空间的偏差正比于 $\|\hat{L} - L\|/\delta_k$，其中 $\delta_k$ 是第 $k$ 和第 $k+1$ 个特征值之间的间距。间距越大，聚类越准确——这解释了为什么谱间距在聚类质量分析中扮演关键角色。

**社区检测（Community Detection）。** 在随机块模型（Stochastic Block Model）中，具有 $n$ 个节点和 $k$ 个社区的网络的邻接矩阵 $A$ 可以分解为期望矩阵 $P$（秩为 $k$）加噪声矩阵 $E$。信号矩阵 $P$ 的算子范数为 $O(n)$，而噪声 $E$ 的算子范数通常为 $O(\sqrt{n})$。Davis--Kahan 定理保证，当信噪比 $O(\sqrt{n})$ 足够大时，从观测邻接矩阵中提取的特征向量能够准确恢复社区结构。这一分析是谱方法在网络科学中广泛应用的理论基石。

**随机矩阵理论中的信号检测。** 在 spiked covariance model（即协方差矩阵为单位阵加低秩扰动）中，Davis--Kahan 定理为分析信号特征向量（spike eigenvectors）与噪声特征向量的分离提供了基本工具，与 Baik--Ben Arous--Peche（BBP）相变现象的研究密切相关。

**矩阵补全和推荐系统。** 在 Netflix 问题等低秩矩阵恢复任务中，从部分观测中恢复的矩阵可以看作是真实矩阵的扰动版本。Davis--Kahan 和 Wedin 定理用于分析恢复的奇异子空间的准确性，是 Candes--Recht（2009）和 Candes--Tao（2010）等经典矩阵补全理论的核心工具之一。

---

## 10. 通俗解读

想象你手持一枚精密指南针，它的指针始终指向"真北"——这个方向就像矩阵 $A$ 的特征子空间。现在，有人在指南针旁边放了一块小磁铁（扰动 $E$），指针会偏转一个角度 $\theta$。

Davis--Kahan 定理告诉我们两件事：

第一，偏转角度 $\theta$ 正比于磁铁的强度（$\|E\|$）。磁铁越强，偏转越大，这符合直觉。

第二，偏转角度反比于指南针本身"抵抗偏转"的能力。在矩阵理论中，这种"抵抗力"就是特征值间距 $\delta$——目标特征值群与其余特征值之间的距离。间距越大，特征子空间越"稳固"，越不容易被扰动"转偏"。就像一枚在强地磁场中的指南针比一枚在弱地磁场中的指南针更不容易被小磁铁干扰。

进一步来说，如果我们有多个指南针组成的"指南针阵列"（对应多维特征子空间），那么每个指南针都会偏转一个角度——这些角度就是"典范角"。Davis--Kahan 定理保证，所有这些偏转角度的"总量"（无论用哪种合理的度量方式）都不会超过磁铁强度除以指南针的内在稳定性。

当间距 $\delta$ 很大而扰动 $\|E\|$ 很小时，$\sin\theta \le \|E\|/\delta$ 接近零，意味着特征子空间几乎不动。反之，当 $\delta$ 接近零（特征值几乎重合），即使很小的扰动也可能导致特征子空间发生剧烈旋转——就像在磁极附近，指南针变得极其不稳定。这也解释了为什么在数值计算中，"几乎重复的特征值"是一个如此棘手的问题。

---

## 11. 阅读指南

对于希望深入理解 Davis--Kahan 定理的读者，建议按以下路径循序渐进：

**入门阶段。** 首先推荐 Daniel Hsu 的哥伦比亚大学讲义 "Notes on Matrix Perturbation and Davis-Kahan sin(Theta) Theorem"（2016），它用不到 5 页的篇幅给出了定理的清晰陈述和简洁证明。Yu--Wang--Samworth（2015）发表在 *Biometrika* 上的论文也是极佳的入门材料，仅 9 页，尤其适合统计学和机器学习背景的读者。

**系统学习。** Stewart 和 Sun 的 *Matrix Perturbation Theory*（Academic Press, 1990）是该领域无可争议的标准教材，全书 365 页，第四章和第五章系统讨论了特征值和特征子空间的扰动理论，包括 Davis--Kahan 定理的完整证明和多种推广形式。Rajendra Bhatia 的 *Matrix Analysis*（Springer, 1997）从更抽象的角度讨论了同一主题，利用 majorization 理论和对称规范函数给出了更为优雅的证明。Bhatia 的另一本较短的著作 *Perturbation Bounds for Matrix Eigenvalues*（SIAM, 1987/2007）也值得一读，它更加聚焦于扰动界本身。

**原始文献。** Davis 和 Kahan 的原始论文（1970）长达 46 页，既有深度又有广度，但证明技术较为复杂，符号系统也与现代用法有所不同。建议在掌握基本结果后再回到原文，欣赏作者的几何洞察和严格推导。同时建议阅读 Davis 的前两篇论文（1963, 1965）以了解思想的演进脉络——从第一篇的初步框架到第三篇的完备理论，可以清晰地看到核心思想如何在近十年间逐步成熟。

**前沿进展。** 关注 Fan--Wang--Zhong（2018）的 $\ell_\infty$ 扰动界及其在稳健协方差估计中的应用；Cai--Zhang（2018）关于奇异子空间扰动界最优速率的工作；以及 Eldridge--Belkin（2018）的 "Unperturbed: Spectral Analysis Beyond Davis--Kahan" 一文，后者探索了超越传统 Davis--Kahan 框架的新方法。

---

## 12. 局限性

尽管 Davis--Kahan 定理是一个深刻而优美的结果，它也有明确的局限性，这些局限性推动了后续大量改进工作的产生。

**间距条件 $\delta > 0$ 是必要的。** 当目标特征值簇与其余特征值之间没有间距（$\delta = 0$），或间距极小时，上界 $\|E\|/\delta$ 可以任意大（甚至超过 1，此时 $\sin\Theta$ 的上界超过其最大可能值，估计变得平凡）。这意味着对于重特征值或接近特征值的情形，定理无法给出有用的信息。在实际应用中，当数据的信噪比较低时，特征值间距可能很小，Davis--Kahan 定理的上界可能过于保守。

**最坏情况估计的保守性。** 定理给出的是最坏情况的上界，不考虑扰动 $E$ 的具体结构。在实际应用中，扰动往往具有特殊结构——例如在统计问题中，$E = \hat{\Sigma} - \Sigma$ 是一个随机矩阵，其谱性质远比一般确定性矩阵更为受限。在这些情况下，可能存在比 Davis--Kahan 上界更紧的估计。近年来的"非对称"或"随机扰动"下的精细分析（如 random matrix perturbation theory）正是为了在特定结构下突破最坏情况的限制。

**仅适用于 Hermite 矩阵。** 原始定理严格要求 $A$ 和 $\tilde{A}$ 均为 Hermite 矩阵（即自伴算子）。对于一般矩阵的不变子空间扰动，需要使用 Wedin 定理（奇异子空间）或 Stewart 的广义 sin Theta 定理。对于非正规矩阵（non-normal matrices），情况更为复杂，特征子空间的敏感性可能远超 Hermite 情形。

**$\ell_2$/Frobenius 范数的局限。** 经典 Davis--Kahan 定理在 $\ell_2$ 或 Frobenius 范数下控制子空间偏差，但不能直接给出逐行（entrywise）或逐列的精细控制。这在高维统计的某些应用中是一个实质性的限制。例如，在社区检测中，Frobenius 范数控制意味着大部分节点被正确分类，但不能排除少量节点被严重错分的可能。近年来 Fan 等人的 $\ell_\infty$ 推广正是为了弥补这一不足。

---

## 13. 延伸阅读

1. **Davis, C.** (1963). The rotation of eigenvectors by a perturbation. *J. Math. Anal. Appl.*, 6, 159--173.（系列第一篇，Davis 独著，奠定基本框架）

2. **Davis, C.** (1965). The rotation of eigenvectors by a perturbation. II. *J. Math. Anal. Appl.*, 11, 20--27.（系列第二篇，技术改进）

3. **Wedin, P.-A.** (1972). Perturbation bounds in connection with singular value decomposition. *BIT Numerical Mathematics*, 12, 99--111.（将 sin Theta 定理推广到奇异子空间，影响深远）

4. **Kato, T.** (1966). *Perturbation Theory for Linear Operators*. Springer.（算子扰动理论的百科全书式著作，提供了理论框架）

5. **Stewart, G. W. & Sun, J.-G.** (1990). *Matrix Perturbation Theory*. Academic Press.（矩阵扰动理论的标准教材，对 Davis--Kahan 定理有最系统的综合）

6. **Bhatia, R.** (1997). *Matrix Analysis*. Springer.（从算子不等式和 majorization 角度讨论扰动理论，证明优雅）

7. **Yu, Y., Wang, T., & Samworth, R. J.** (2015). A useful variant of the Davis--Kahan theorem for statisticians. *Biometrika*, 102(2), 315--323.（适合统计应用的重要变体，被大量后续工作引用）

8. **Cai, T. T. & Zhang, A.** (2018). Rate-optimal perturbation bounds for singular subspaces with applications to high-dimensional statistics. *Annals of Statistics*, 46(1), 60--89.（证明了最优扰动速率，确立了 Davis--Kahan 框架的最优性）

---

## 14. 参考文献

- Davis, C. & Kahan, W. M. (1970). The rotation of eigenvectors by a perturbation. III. *SIAM Journal on Numerical Analysis*, 7(1), 1--46.
- Davis, C. (1963). The rotation of eigenvectors by a perturbation. *Journal of Mathematical Analysis and Applications*, 6, 159--173.
- Davis, C. (1965). The rotation of eigenvectors by a perturbation. II. *Journal of Mathematical Analysis and Applications*, 11, 20--27.
- Weyl, H. (1912). Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen. *Mathematische Annalen*, 71, 441--479.
- Hoffman, A. J. & Wielandt, H. W. (1953). The variation of the spectrum of a normal matrix. *Duke Mathematical Journal*, 20(1), 37--39.
- Kato, T. (1966). *Perturbation Theory for Linear Operators*. Springer-Verlag.
- Wedin, P.-A. (1972). Perturbation bounds in connection with singular value decomposition. *BIT Numerical Mathematics*, 12, 99--111.
- Stewart, G. W. & Sun, J.-G. (1990). *Matrix Perturbation Theory*. Academic Press.
- Bhatia, R. (1997). *Matrix Analysis*. Springer.
- Yu, Y., Wang, T., & Samworth, R. J. (2015). A useful variant of the Davis--Kahan theorem for statisticians. *Biometrika*, 102(2), 315--323.
- Fan, J., Wang, W., & Zhong, Y. (2018). An $\ell_\infty$ eigenvector perturbation bound and its application to robust covariance estimation. *Journal of Machine Learning Research*, 18, 1--42.
- Cai, T. T. & Zhang, A. (2018). Rate-optimal perturbation bounds for singular subspaces with applications to high-dimensional statistics. *Annals of Statistics*, 46(1), 60--89.
- Wilkinson, J. H. (1965). *The Algebraic Eigenvalue Problem*. Oxford University Press.
