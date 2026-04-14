# Von Neumann 迹不等式（1937）：奇异值与矩阵内积的深层联系

## 1. 作者

**John von Neumann**（约翰·冯·诺依曼，1903年12月28日 -- 1957年2月8日）

匈牙利裔美国数学家、物理学家、计算机科学奠基人。1903年生于布达佩斯一个富裕的犹太银行家家庭，自幼展现出惊人的数学天赋。他先后在柏林大学、苏黎世联邦理工学院和布达佩斯大学求学，于1926年几乎同时获得布达佩斯大学数学博士学位和苏黎世联邦理工学院化学学士学位。1930年赴 Princeton 大学任访问讲师，1933年成为新成立的 Princeton 高等研究院（Institute for Advanced Study, IAS）最早的五位教授之一——另一位是 Albert Einstein。von Neumann 的学术贡献横跨纯数学、量子力学、博弈论、算子代数、计算机体系结构和数值分析等诸多领域，被公认为20世纪最伟大的数学全才之一。

## 2. 发表时间与刊物

**1937年**，发表于 *Tomsk University Review*（全称 *Mitteilungen des Forschungsinstituts fur Mathematik und Mechanik, Universitat Tomsk*），卷1，第286--300页。

论文标题为 "Some matrix-inequalities and metrization of matric-space"。该文后被收入 A. H. Taub 主编的 *John von Neumann Collected Works* 第四卷（Pergamon Press, 1962年），第205--218页。

值得注意的是，这篇具有深远影响的论文发表在苏联西伯利亚城市 Tomsk 的大学刊物上，这在当时并非罕见——1930年代的国际数学界保持着相当活跃的跨国交流，即便是在政治局势日趋紧张的年代。论文发表于一个相对小众的刊物，但其核心结果的重要性使之迅速为国际数学界所知晓，并在随后数十年中被反复引用和推广。

## 3. 一句话概括

建立了两个矩阵迹内积与它们奇异值序列之间的精确不等式关系，揭示了矩阵内积的最优上界由奇异值的有序配对决定。

## 4. 历史背景

20世纪30年代是矩阵理论、泛函分析与量子力学三大学科交汇融合的黄金时期。要理解 von Neumann 迹不等式诞生的历史语境，需要从多个维度加以考察。

**矩阵理论的成熟期**。19世纪末至20世纪初，矩阵理论经历了从具体计算工具到抽象代数结构的深刻转变。Cayley、Sylvester 奠定了矩阵代数的基本框架，而 Frobenius、Schur 等人则将矩阵理论推向了更高的抽象层次。特别是 Issai Schur 于1909年证明的酉三角化定理——任何方阵都可以通过酉相似变换化为上三角矩阵——为矩阵谱理论的发展提供了关键的技术工具。与此同时，奇异值的概念正在逐步形成：Erhard Schmidt 在1907年研究非对称积分方程时引入了"伴随特征函数"的概念，这实质上就是奇异值分解在无穷维空间中的先驱形态。Picard 在1910年的后续工作中首次使用了"奇异值"这一术语（尽管这一名称的正式确立要等到 Smithies 在1937年的工作）。在有限维空间中，Beltrami（1873）、Jordan（1874）和 Sylvester（1889）实际上已经独立发现了奇异值分解的基本形式，尽管他们使用的是不同的数学语言。

**泛函分析的兴起**。David Hilbert 在20世纪初创立了以其名字命名的 Hilbert 空间理论，von Neumann 在1926至1927年间作为 Hilbert 在 Gottingen 的助手，为量子力学建立了严格的数学基础。这段经历深刻影响了 von Neumann 对算子理论的理解。他认识到，矩阵不仅仅是数表，更是 Hilbert 空间上线性算子的有限维表示。这种观点使他自然地关注那些在酉变换下保持不变的量——这正是迹不等式的核心主题。1930年代中期，von Neumann 与 F. J. Murray 合作开创了算子代数（后被命名为 von Neumann 代数）理论，系统研究了算子的各种不变量和范数结构。

**量子力学的数学化**。von Neumann 于1932年出版的 *Mathematische Grundlagen der Quantenmechanik*（量子力学的数学基础）一书，将量子力学建立在 Hilbert 空间的严格公理化框架之上。在量子力学中，可观测量对应于 Hermite 算子，而状态的叠加和测量过程都涉及迹运算。这种物理背景使 von Neumann 特别关注迹函数的性质，以及矩阵的内在谱数据（特征值和奇异值）如何控制各种矩阵运算的结果。

**酉不变范数的需求**。1930年代的数学家们逐渐认识到，在许多应用中，矩阵的"大小"不应依赖于坐标系的选择，即应在酉变换下保持不变。这种认识催生了对酉不变范数系统理论的需求。von Neumann 正是在这一背景下，试图用矩阵的内在不变量——奇异值——来刻画所有可能的酉不变范数和矩阵内积。1937年的迹不等式论文正是这一宏大目标的关键一步：它建立了迹内积（矩阵空间上最自然的内积之一）与奇异值之间的精确定量关系。

## 5. 核心问题

von Neumann 在这篇论文中面对的核心问题可以简洁地表述为：

**给定两个 n x n 复矩阵 A 和 B，它们的迹内积 tr(A\*B) 的绝对值最大能有多大？这个最大值如何用矩阵的内在谱信息——即奇异值——来精确刻画？**

更具体地说，von Neumann 考虑的问题包含两个层次。第一个层次是上界问题：寻找 |tr(A\*B)| 的一个仅依赖于 A 和 B 各自奇异值的最优上界。第二个层次是极值问题：当 A 的奇异值固定时，max |tr(UB)|（U 取遍所有酉矩阵）能否用 B 的奇异值精确表达？这两个层次的问题在数学上是紧密关联的，它们共同指向一个根本性的结构问题：迹函数在酉群作用下的极值行为。

这一问题的深层动机来自于矩阵空间的度量化（metrization of matric-space）。正如论文标题所暗示的，von Neumann 不仅关心一个具体的不等式，更关心如何利用奇异值在矩阵空间上定义自然的度量和范数结构。

## 6. 主要定理与结果

### Von Neumann 迹不等式

设 A 和 B 为任意 n x n 复矩阵，其奇异值分别按降序排列为

sigma\_1(A) >= sigma\_2(A) >= ... >= sigma\_n(A) >= 0,

sigma\_1(B) >= sigma\_2(B) >= ... >= sigma\_n(B) >= 0,

则

**|tr(A\*B)| <= sum\_{i=1}^{n} sigma\_i(A) sigma\_i(B).**

这里 A\* 表示 A 的共轭转置，tr 表示矩阵的迹。

### 等号条件

等号成立的充要条件是：存在酉矩阵 U 和 V，使得 A = U Sigma\_A V\* 和 B = U Sigma\_B V\*，即 A 和 B 可以被同一对酉矩阵同时奇异值分解。换言之，A 和 B\* 共享左右奇异向量。这意味着当且仅当两个矩阵的"主轴方向"完全对齐时，它们的迹内积达到最大值。

### 等价的极值形式

von Neumann 还证明了如下等价形式：对于固定的复矩阵 A（奇异值为 sigma\_1(A) >= ... >= sigma\_n(A)），当 U 和 V 取遍所有 n x n 酉矩阵时，

max\_{U,V 为酉矩阵} Re tr(U A V B) = sum\_{i=1}^{n} sigma\_i(A) sigma\_i(B).

这一形式清楚地展示了迹不等式的几何意义：它描述了矩阵在酉群轨道上的极值行为。

### 与酉不变范数的联系

von Neumann 在同一篇论文中还建立了酉不变范数与对称规范函数（symmetric gauge functions）之间的一一对应关系。具体而言，他证明了矩阵空间上的范数 |||.| || 是酉不变的（即 |||UAV||| = |||A||| 对所有酉矩阵 U, V 成立）当且仅当存在向量空间 R^n 上的一个对称规范函数 g，使得 |||A||| = g(sigma\_1(A), ..., sigma\_n(A))。所谓对称规范函数，是指一个关于坐标置换不变且关于符号变换不变的范数。迹不等式正是这一对应关系的核心工具。

## 7. 核心方法

von Neumann 的原始证明综合运用了多种精巧的数学技术，展现了他标志性的深刻洞察力。

### 奇异值分解（SVD）

证明的第一步是利用奇异值分解将问题标准化。任何 n x n 复矩阵 A 都可以分解为 A = U\_A Sigma\_A V\_A\*，其中 U\_A 和 V\_A 是酉矩阵，Sigma\_A 是以奇异值为对角元素的非负对角矩阵。将 A 和 B 同时进行 SVD 后，迹 tr(A\*B) 可以表示为奇异值与酉矩阵内积的组合形式。

### 酉群上的极值分析

证明的核心在于分析迹函数在酉群上的极值行为。将 SVD 代入后，问题转化为：对于给定的非负对角矩阵 Sigma\_A 和 Sigma\_B，如何最大化 |tr(Sigma\_A W Sigma\_B)| 或 Re tr(Sigma\_A W Sigma\_B)，其中 W = V\_A U\_B\* 取遍酉群。这是一个酉群上的优化问题。von Neumann 利用了酉矩阵元素的模的平方构成双随机矩阵这一关键性质。

### 双随机矩阵与 Birkhoff 定理的联系

设 W 是一个酉矩阵，定义矩阵 M，其元素为 M\_{ij} = |W\_{ij}|^2。由酉矩阵的行列正交归一性质可知，M 的每行每列元素之和均为1，且所有元素非负，因此 M 是一个双随机矩阵（doubly stochastic matrix）。根据 Birkhoff 定理（1946年由 Garrett Birkhoff 正式证明，von Neumann 本人后来在1953年也给出了独立证明），每个双随机矩阵都是置换矩阵的凸组合。

利用这一结构，可以证明：

Re tr(Sigma\_A W Sigma\_B) = sum\_{i,j} sigma\_i(A) sigma\_j(B) Re(W\_{ij}) <= sum\_{i,j} sigma\_i(A) sigma\_j(B) |W\_{ij}|^2 的适当放缩.

通过 Birkhoff 定理，这个和式在 M 为单位置换矩阵（即恒等排列）时取最大值，从而得到 sum\_i sigma\_i(A) sigma\_i(B)。直观地说，奇异值的最优配对方式是"大配大、小配小"——按降序排列后逐项相乘求和。

### 后续的简化证明

von Neumann 的原始证明相当复杂。正如 P. G. Ciarlet 所评论的："出人意料的是，为这个看似简单的结果找到一个像样的证明远非易事。"1975年，L. Mirsky 在 *Monatshefte fur Mathematik* 上发表了一个自足的简化证明，明确利用了双随机矩阵的凸分解性质。Mirsky 的证明使这一定理变得更加易于理解和传授，成为现代教科书中最常见的证明方式。

## 8. 重要性与影响

von Neumann 迹不等式的重要性远远超出了一个具体不等式本身，它在矩阵分析的多个核心领域都发挥着基石性的作用。

**奇异值理论的核心定理**。迹不等式揭示了一个深刻的结构性事实：矩阵迹内积——作为矩阵空间上最自然的"角度"或"相关性"度量——完全被奇异值所控制。这意味着奇异值不仅仅是矩阵的一组数值不变量，更是理解矩阵之间相互关系的核心工具。在迹不等式出现之前，虽然人们已经知道奇异值的存在和基本性质，但尚未充分认识到它们在矩阵关系理论中的中心地位。

**酉不变范数理论的基石**。von Neumann 在同一篇论文中建立的酉不变范数与对称规范函数之间的对应关系，为整个酉不变范数理论奠定了基础。这一理论后来在 Robert Schatten 的 *Norm Ideals of Completely Continuous Operators*（1960年）中得到了系统化的发展，形成了以 Schatten--von Neumann 范数命名的重要范数族。迹不等式是连接抽象范数理论与具体奇异值计算的桥梁。

**矩阵逼近理论的理论基础**。迹不等式为 Eckart--Young 定理（1936年）——截断 SVD 给出最优低秩逼近——提供了更深层的理论视角。通过迹不等式，可以统一理解为什么在各种酉不变范数下，SVD 都给出最优逼近。L. Mirsky 在1960年将 Eckart--Young 定理从 Frobenius 范数和谱范数推广到所有酉不变范数，其论证正是基于 von Neumann 的框架。

**弹性力学与连续介质力学**。在应用数学领域，迹不等式在 J. M. Ball 关于非线性弹性方程的存在性理论中发挥了关键作用。Ball 利用迹不等式来控制变形梯度张量的性质，从而建立弹性体平衡态的存在性。这一应用展示了纯粹矩阵理论如何深刻地影响物理和工程科学。

**Schatten 理论与交叉空间**。Schatten 在发展完全连续算子的范数理想理论时，将迹不等式作为核心技术工具。Schatten 类算子（trace class, Hilbert--Schmidt class 等）的基本性质——包括对偶性、插值和分解定理——都以迹不等式为关键步骤。

## 9. 解决了什么瓶颈

在 von Neumann 1937年的工作之前，矩阵理论面临一个关键的概念瓶颈：**缺乏将迹内积与矩阵的内在谱数据精确联系起来的系统性工具**。

具体而言，数学家们已经知道单个矩阵的许多谱性质——特征值的分布、奇异值的存在性、矩阵的各种分解形式——但对于**两个矩阵之间的相互作用**如何被它们各自的谱数据所控制，理解却相当有限。迹 tr(AB) 涉及 A 和 B 的元素的复杂组合，从表面上看，它似乎不应该仅由各自的奇异值就能精确控制。von Neumann 的不等式恰好填补了这一空白，证明了一个出人意料的结论：尽管迹内积依赖于矩阵的全部信息（包括奇异向量的方向），其绝对值的最优上界却仅取决于奇异值本身。

此外，在1937年之前，矩阵空间上的距离和范数结构尚未被系统化。虽然 Frobenius 范数和谱范数已为人所知，但它们只是酉不变范数大家族中的特例。von Neumann 的工作为矩阵空间的度量化提供了统一框架，使得后来的研究者能够系统地构造和分类各种酉不变范数。

## 10. 与前人工作的关系

von Neumann 的迹不等式并非凭空产生，而是建立在19世纪末至20世纪初一系列重要工作的基础之上。

**Erhard Schmidt（1907）的奇异值概念**。Schmidt 在研究非对称积分方程时，引入了成对的"伴随特征函数"和相应的正特征值，这实质上就是奇异值分解在积分算子情形下的雏形。Schmidt 还证明了后来以 Eckart--Young 命名的低秩逼近定理的无穷维版本——正如 G. W. Stewart 在1993年的历史综述中所指出的，"我们真的不应该把 SVD 的逼近定理称为 Eckart--Young 定理，因为 Schmidt 才是更早证明它的人。"von Neumann 的工作可以被视为 Schmidt 奇异值理论在有限维矩阵空间中的进一步发展和深化。

**Hermann Weyl 的特征值不等式**。Weyl 在1912年建立了 Hermite 矩阵特征值的扰动不等式，并在1949年发表了将特征值与奇异值联系起来的关键不等式——"Inequalities between the Two Kinds of Eigenvalues of a Linear Transformation"（*Proceedings of the National Academy of Sciences*）。虽然 Weyl 1949年的论文晚于 von Neumann 的1937年工作，但 Weyl 关于特征值稳定性的早期思想（1912年）对 von Neumann 有直接的影响。两人在 Princeton 高等研究院的长期共事关系也促进了思想的交流。

**Issai Schur 的酉三角化定理**。Schur 于1909年证明了任何方阵都可以通过酉相似变换化为上三角矩阵。这一定理为 von Neumann 分析迹函数在酉群作用下的行为提供了技术基础。

**Beltrami、Jordan、Sylvester 的有限维 SVD**。尽管奇异值分解的有限维形式早在1870年代就由 Beltrami（1873）和 Jordan（1874）独立发现，但这些早期工作主要关注分解的存在性，而非奇异值的不等式性质。von Neumann 的贡献在于揭示了奇异值在控制矩阵运算中的定量作用。

## 11. 对后续工作的影响

von Neumann 的迹不等式开创了矩阵不等式理论的一个重要分支，对后续半个多世纪的研究产生了深远影响。

**Mirsky 不等式（1975）**。L. Mirsky 不仅给出了 von Neumann 迹不等式的简化证明，还在1960年将 Eckart--Young 低秩逼近定理从 Frobenius 范数和谱范数推广到所有酉不变范数。这一推广直接依赖于 von Neumann 建立的酉不变范数框架。

**Lidskii 定理（1950）**。V. B. Lidskii 在1950年发表了关于对称矩阵之和与积的特征值的不等式。Lidskii 定理可以视为 von Neumann 迹不等式在 Hermite 矩阵特征值领域的"对偶"版本，两者共同构成了矩阵谱理论的两大支柱。

**Ky Fan 范数不等式（1949--1951）**。Ky Fan 在 von Neumann 框架的基础上，引入了以其名字命名的 Ky Fan k-范数（前 k 个最大奇异值之和），并建立了一系列基本不等式。Fan 还证明了 von Neumann 关于酉不变范数的刻画定理可以从他的工作中简洁地推出。Fan 与 A. J. Hoffman 在1955年的合作论文 "Some metric inequalities in the space of matrices" 进一步发展了矩阵空间的度量理论。

**Schatten 类与理想理论**。Robert Schatten 在1950--1960年代系统发展了完全连续算子的范数理想理论，将有限维的 von Neumann 框架推广到无穷维 Hilbert 空间上。由此产生的 Schatten--von Neumann 范数（或 Schatten p-范数）成为泛函分析中不可或缺的工具，其中 Schatten 1-范数即核范数（trace norm），Schatten 2-范数即 Hilbert--Schmidt 范数，Schatten 无穷范数即算子范数。

**Kristof 的推广（1969）**。W. Kristof 将 von Neumann 关于两个矩阵的迹不等式推广到多个矩阵乘积的情形，即考虑 tr(Z\_1 A\_1 Z\_2 A\_2 ... Z\_n A\_n) 当 Z\_i 取遍酉矩阵时的极值。

**Horn 猜想与现代发展**。von Neumann 的工作间接推动了 Horn 猜想的提出和最终解决。Horn 猜想完整描述了两个 Hermite 矩阵之和的特征值的所有约束条件，其最终证明（由 Klyachko 和 Knutson--Tao 在1990年代末完成）涉及了代数几何、表示论和组合数学等多个领域的深刻工具，被 Terence Tao 称为"一个引人入胜的故事"。

## 12. 现代价值

在当代数学和计算科学中，von Neumann 迹不等式的思想和技术继续焕发着强大的生命力，尤其在以下几个领域。

**低秩矩阵逼近与数据压缩**。迹不等式为 SVD 低秩逼近的最优性提供了理论保证。在现代大数据时代，低秩矩阵逼近是数据压缩、降维和去噪的核心技术。图像压缩（如 JPEG 2000 中使用的技术）、信号处理中的子空间方法、以及基因组数据分析中的降维技术，都直接或间接地依赖于 von Neumann 建立的理论框架。

**推荐系统与矩阵补全**。Netflix Prize 竞赛（2006--2009）使矩阵补全问题进入了公众视野。推荐系统的核心任务——从用户对少量商品的评分中推断其对所有商品的偏好——可以建模为低秩矩阵的补全问题。在求解这一问题时，核范数（即所有奇异值之和，也就是 Schatten 1-范数）被用作矩阵秩的凸松弛。核范数正则化方法的理论基础正是 von Neumann 关于酉不变范数的框架。Emmanuel Candes 和 Benjamin Recht 在2009年证明的矩阵补全理论保证——在适当的不相干条件下，通过核范数最小化可以从少量观测中精确恢复低秩矩阵——可以被视为 von Neumann 思想在现代优化理论中的延伸。

**主成分分析（PCA）**。PCA 是统计学和机器学习中最基本的降维方法之一，其数学本质就是对数据矩阵进行 SVD 并取前 k 个奇异值对应的分量。von Neumann 迹不等式保证了这种做法在迹内积意义下的最优性：截断 SVD 所保留的"信息量"（用迹内积度量）是所有同秩矩阵中最大的。

**核范数正则化与压缩感知**。在现代机器学习和信号处理中，核范数正则化是处理矩阵结构数据的标准技术。正如 L1 范数正则化产生稀疏解，核范数正则化产生低秩解。这一类比的数学基础可以追溯到 von Neumann 对奇异值作为矩阵"坐标"的深刻理解。在多任务学习、矩阵分类、稳健 PCA 等问题中，核范数正则化都扮演着关键角色。

**量子信息理论**。在量子信息科学中，密度矩阵的迹范数（Schatten 1-范数）是量化量子态之间可区分度的基本度量，而迹不等式为量子信道容量、纠缠度量等核心概念提供了数学工具。这一应用领域恰好呼应了 von Neumann 最初从量子力学出发的思想动机。

## 13. 通俗解读

von Neumann 迹不等式的核心思想可以用一个直观的"投影匹配"比喻来理解。

想象你有两组聚光灯，分别照向不同的方向。每组灯有若干盏，亮度各不相同。第一组灯的亮度分别是 sigma\_1(A), sigma\_2(A), ...（从亮到暗排列），第二组是 sigma\_1(B), sigma\_2(B), ...。现在，你可以自由旋转每组灯的整体方向，问题是：两组灯照出的光斑重叠面积（即"相互作用"程度）最大能有多大？

von Neumann 的答案是：最大重叠发生在**两组灯的方向完全对齐**时——最亮的灯对最亮的灯，次亮的对次亮的，以此类推。此时总重叠量恰好等于 sigma\_1(A) sigma\_1(B) + sigma\_2(A) sigma\_2(B) + ...。

这个结论之所以有些出人意料，是因为直觉上你可能会想：也许某种"巧妙的错位"能让几盏中等亮度的灯同时与一盏很亮的灯重叠，从而获得更大的总效果？von Neumann 严格证明了这种投机取巧不可能奏效——"大配大、小配小"的有序配对永远是最优策略。

用更数学化的语言说：迹 tr(A\*B) 可以视为矩阵 A 和 B 之间的"广义内积"，它度量了两个矩阵在某种意义上的"相似程度"。奇异值则刻画了矩阵沿各个主方向的"伸缩强度"。迹不等式告诉我们，这种相似程度完全被各方向上伸缩强度的匹配程度所控制——即使两个矩阵的主方向完全不同，它们的迹内积也不可能超过对应奇异值乘积之和。

## 14. 阅读指南

对于希望深入理解 von Neumann 迹不等式的读者，建议按以下路径循序渐进：

**入门级**（线性代数基础）：首先确保掌握矩阵的基本运算（迹、转置、共轭转置）、特征值和特征向量的概念。推荐 Gilbert Strang 的 *Introduction to Linear Algebra*。

**基础级**（奇异值分解）：在理解 SVD 的定义、存在性和几何意义后，再来阅读迹不等式的陈述。推荐 Lloyd N. Trefethen 和 David Bau III 的 *Numerical Linear Algebra*，其中 SVD 的讲解清晰而深入。

**进阶级**（迹不等式的证明）：Mirsky 1975年的论文 "A trace inequality of John von Neumann"（*Monatshefte fur Mathematik*, 79, 303--306）是最佳的入门证明材料，只有4页，自足且清晰。与之配合，可以阅读 Birkhoff 定理的标准证明（大多数组合优化教材都有涵盖）。

**高级**（系统性理论）：Roger A. Horn 和 Charles R. Johnson 的经典教科书 *Matrix Analysis*（Cambridge University Press, 第二版2012年）和 *Topics in Matrix Analysis*（1991年）对迹不等式、酉不变范数和奇异值不等式有最为系统的处理。Rajendra Bhatia 的 *Matrix Analysis*（Springer GTM 169, 1997年）则从算子理论的视角给出了深刻的现代处理。

**应用导向**：对于关心现代应用的读者，推荐 Benjamin Recht, Maryam Fazel 和 Pablo A. Parrilo 的 "Guaranteed Minimum-Rank Solutions of Linear Matrix Equations via Nuclear Norm Minimization"（*SIAM Review*, 2010）作为矩阵补全和核范数正则化的入门读物。

## 15. 局限性

尽管 von Neumann 迹不等式是矩阵分析中最优美的结果之一，它仍然有一些固有的局限性和需要注意的方面。

**有限维限制**。原始形式的迹不等式仅适用于有限维矩阵。将其推广到无穷维 Hilbert 空间上的紧算子或 Hilbert--Schmidt 算子需要额外的技术条件（如算子必须属于适当的 Schatten 类），且证明方法也需要相应调整。这一推广在2020年的一篇 *Linear and Multilinear Algebra* 论文中得到了严格处理。

**等号条件的实际验证**。迹不等式的等号条件要求两个矩阵共享奇异向量，这在实际应用中往往难以直接验证。特别是在数值计算中，由于浮点运算的舍入误差，精确的等号几乎不可能实现，只能在近似意义下讨论。

**非交换结构的限制**。迹不等式本质上利用了迹函数的酉不变性和矩阵空间的特殊结构。当试图将类似的不等式推广到更一般的代数结构（如半单 Lie 群上的矩阵不等式）时，需要全新的工具和方法。Tam 等人在2015年将 von Neumann 迹不等式推广到半单 Lie 群的工作，展示了这种推广的非平凡性。

**仅提供上界**。迹不等式只给出 |tr(A\*B)| 的上界，而没有给出下界。在某些应用中（例如矩阵乘积奇异值的估计），下界信息同样重要。Ruhe 在1970年的工作补充了正定矩阵情形下的下界结果。

## 16. 延伸阅读

1. **Mirsky, L.** "A trace inequality of John von Neumann." *Monatshefte fur Mathematik*, 79, 303--306, 1975. 最简洁的自足证明，推荐作为学习迹不等式的首选材料。

2. **Horn, R. A. & Johnson, C. R.** *Matrix Analysis*. Cambridge University Press, 第二版, 2012. 矩阵分析领域最权威的教科书，包含迹不等式及其推广的系统论述。

3. **Bhatia, R.** *Matrix Analysis*. Springer GTM 169, 1997. 从算子理论视角对矩阵不等式的深刻处理，特别适合有泛函分析背景的读者。

4. **Stewart, G. W.** "On the early history of the singular value decomposition." *SIAM Review*, 35(4), 551--566, 1993. SVD 发展史的权威综述，详细追溯了从 Beltrami 到 Schmidt 的历史脉络。

5. **Fan, K.** "Maximum properties and inequalities for the eigenvalues of completely continuous operators." *Proceedings of the National Academy of Sciences*, 37(11), 760--766, 1951. Ky Fan 范数理论的奠基之作，是 von Neumann 框架的重要发展。

6. **Schatten, R.** *Norm Ideals of Completely Continuous Operators*. Springer, 1960. 将 von Neumann 的有限维理论推广到无穷维空间的经典专著。

7. **Candes, E. J. & Recht, B.** "Exact matrix completion via convex optimization." *Foundations of Computational Mathematics*, 9(6), 717--772, 2009. 核范数在矩阵补全中的理论保证，von Neumann 思想的现代应用典范。

8. **Grigorieff, R. D.** "A note on von Neumann's trace inequality." *Mathematische Nachrichten*, 151, 327--328, 1991. 对迹不等式的进一步注释和简化。

## 17. 参考文献

[1] von Neumann, J. "Some matrix-inequalities and metrization of matric-space." *Tomsk University Review* (*Mitteilungen des Forschungsinstituts fur Mathematik und Mechanik, Universitat Tomsk*), 1, 286--300, 1937. 收入 A. H. Taub (Ed.), *John von Neumann Collected Works*, Vol. IV, Pergamon Press, 1962, pp. 205--218.

[2] Schmidt, E. "Zur Theorie der linearen und nichtlinearen Integralgleichungen. I Teil." *Mathematische Annalen*, 63, 433--476, 1907.

[3] Eckart, C. & Young, G. "The approximation of one matrix by another of lower rank." *Psychometrika*, 1, 211--218, 1936.

[4] Mirsky, L. "A trace inequality of John von Neumann." *Monatshefte fur Mathematik*, 79, 303--306, 1975.

[5] Fan, K. "Maximum properties and inequalities for the eigenvalues of completely continuous operators." *Proceedings of the National Academy of Sciences*, 37(11), 760--766, 1951.

[6] Fan, K. & Hoffman, A. J. "Some metric inequalities in the space of matrices." *Proceedings of the American Mathematical Society*, 6(1), 111--116, 1955.

[7] Weyl, H. "Inequalities between the two kinds of eigenvalues of a linear transformation." *Proceedings of the National Academy of Sciences*, 35(7), 408--411, 1949.

[8] Lidskii, V. B. "The proper values of the sum and the product of symmetric matrices." *Doklady Akademii Nauk SSSR*, 74, 769--772, 1950.

[9] Kristof, W. "A generalization of a theorem by John von Neumann on the trace of certain matrix products." *ETS Research Bulletin Series*, 1969.

[10] Birkhoff, G. "Three observations on linear algebra." *Univ. Nac. Tucuman Rev. Ser. A*, 5, 147--151, 1946.

[11] Schatten, R. *Norm Ideals of Completely Continuous Operators*. Springer, 1960.

[12] Horn, R. A. & Johnson, C. R. *Matrix Analysis*. Cambridge University Press, 第二版, 2012.

[13] Bhatia, R. *Matrix Analysis*. Springer GTM 169, 1997.

[14] Stewart, G. W. "On the early history of the singular value decomposition." *SIAM Review*, 35(4), 551--566, 1993.

[15] Candes, E. J. & Recht, B. "Exact matrix completion via convex optimization." *Foundations of Computational Mathematics*, 9(6), 717--772, 2009.
