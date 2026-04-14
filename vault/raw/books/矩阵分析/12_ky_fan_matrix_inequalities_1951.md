# Ky Fan 矩阵不等式（1949--1951）：特征值部分和与范数理论的统一

## 作者

**Ky Fan（樊畿，1914--2010）**，美籍华裔数学家，20 世纪最具影响力的分析学家之一。他的研究横跨线性分析与非线性分析，从有限维延伸到无穷维，从纯数学拓展到应用数学，在泛函分析、凸分析、不等式理论、不动点理论、算子理论、矩阵理论、线性与非线性规划、复分析、拓扑学等领域均有基础性贡献。据 MathSciNet 统计，Ky Fan 一生共发表 126 篇论文和著作，与 15 位数学家合作，指导了 23 名研究生。1964 年当选台湾中央研究院院士，1978 至 1984 年兼任中央研究院数学研究所所长。他毕生热爱祖国，曾多次慷慨捐资促进中国数学事业的发展。

## 发表时间与刊物

- K. Fan, "On a Theorem of Weyl Concerning Eigenvalues of Linear Transformations I," *Proceedings of the National Academy of Sciences*, **35**(11), 652--655, 1949.
- K. Fan, "On a Theorem of Weyl Concerning Eigenvalues of Linear Transformations II," *Proceedings of the National Academy of Sciences*, **36**(1), 31--35, 1950.
- K. Fan, "Maximum Properties and Inequalities for the Eigenvalues of Completely Continuous Operators," *Proceedings of the National Academy of Sciences*, **37**(11), 760--766, 1951.

上述三篇论文均刊发于美国国家科学院院刊（PNAS），这是当时美国最具声望的综合性学术期刊之一。研究工作得到了美国海军研究办公室（Office of Naval Research）的部分资助。

## 一句话概括

建立了 Hermite 矩阵特征值部分和的极值刻画，将 Weyl 的单个特征值不等式提升为部分和控制，统一了特征值不等式与酉不变范数理论。

---

## 一、历史背景

Ky Fan（樊畿）1914 年 9 月 19 日生于杭州，1932 年考入北京大学数学系。他最初有志于学习工程，但受其舅父、时任北京大学数学系主任冯祖荀（1880--1940）的深刻影响，最终转向了数学。在北大求学期间，年轻的樊畿已展露出非凡的数学才华：大学二年级的暑假，他翻译了两本德文教材并将其合编为一本《解析几何与代数》教科书，于 1935 年出版。1936 年获学士学位。据 Ky Fan 本人回忆，他在中学和大学时代"讨厌英语"，这也成为他选择数学--一个"英语少而方程多"的学科--以及选择赴法国而非英语国家留学的重要原因。

1939 年，Ky Fan 赴法国巴黎，师从泛函分析先驱 Maurice Frechet，1941 年在巴黎大学获理学博士学位。此后他在法国国家科学研究中心（CNRS）担任研究员，度过了战争年代。1945 至 1947 年，他获聘为普林斯顿高等研究院成员，在那里与 20 世纪最伟大的数学家中的两位--John von Neumann 和 Hermann Weyl--建立了密切的学术联系。这段经历对他后续的矩阵理论研究产生了决定性影响：von Neumann 1937 年的迹不等式和 Weyl 1912 年的特征值不等式，正是 Ky Fan 1949--1951 年系列工作的直接思想源泉。1947 年起，他加入圣母大学（University of Notre Dame）数学系，正是在这一时期完成了关于矩阵特征值不等式的系列开创性工作。1965 年，他转任加州大学圣塔芭芭拉分校（UCSB）数学教授，直至 1985 年退休。

20 世纪上半叶，谱理论正经历从有限维线性代数向无穷维算子理论的深刻转型。这一转型的驱动力来自多个方面：物理学中量子力学的兴起需要对 Hilbert 空间上自伴算子的谱进行精确刻画；积分方程理论的发展催生了对紧算子特征值分布的系统研究；而统计学中主成分分析等方法也对矩阵特征值的定量估计提出了实际需求。

Hermann Weyl 在 1912 年发表的经典论文《Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen》中，建立了 Hermite 矩阵特征值的扰动不等式，最初动机来自线性偏微分方程特征值的渐近分布以及黑体辐射的理论分析。Ernst Fischer 早在 1905 年就为二次型的最小特征值建立了极大极小刻画，随后 Weyl 在 1909 年将这一思想推广到中间特征值，Richard Courant 在 1920 年代完成了统一的极大极小原理的表述，形成了著名的 Courant-Fischer 极大极小定理。这些经典工具为单个特征值提供了优雅的子空间变分表述。

然而，这些经典工具都局限于对**单个**特征值的控制：Weyl 不等式给出的是 $\lambda_i(A+B)$ 与 $\lambda_j(A)$、$\lambda_k(B)$ 之间的逐项约束，Courant-Fischer 定理也只刻画了第 $k$ 个特征值的极值性质。数学界面临的核心挑战是：能否从单个特征值的控制上升到**特征值组**的整体控制？具体而言，当我们关注矩阵前 $k$ 个最大特征值的**总和**时，是否存在类似的极值原理和不等式？这一问题的回答不仅具有纯数学价值，还与物理学中多粒子系统的能级问题、统计学中的主成分分析等应用密切相关。正是在这样的学术背景下，Ky Fan 于 1949 至 1951 年间发表了三篇里程碑式的论文，完成了从"单个特征值"到"特征值部分和"的理论飞跃。

## 二、核心问题

设 $A$ 和 $B$ 为 $n \times n$ Hermite 矩阵，其特征值按降序排列为 $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_n$。Ky Fan 的核心问题可以表述为：

**矩阵和 $A + B$ 的特征值与 $A$、$B$ 各自的特征值之间，存在怎样的精确定量关系？特别是，前 $k$ 个最大特征值的部分和满足什么样的不等式？这些不等式能否通过极值原理给予内在的变分刻画？**

Weyl 在 1912 年给出的经典结果是逐项不等式：

$$\lambda_{i+j-1}(A+B) \leq \lambda_i(A) + \lambda_j(B), \quad i+j-1 \leq n$$

这一不等式的证明基于 Courant-Fischer 定理和子空间维数论证，控制的是矩阵和的某一个特征值与两个矩阵各取一个特征值之和的关系。但如果我们想要了解"矩阵 $A+B$ 的前 $k$ 个最大特征值的总能量（总和）与 $A$、$B$ 各自前 $k$ 个最大特征值总能量的关系"，Weyl 不等式就力不从心了。

更深层的问题是：特征值的部分和 $\sum_{i=1}^{k} \lambda_i(A)$ 是否像单个特征值 $\lambda_k(A)$ 一样具有内在的变分意义？如果有，这一变分刻画是什么形式？它能否自然地导出部分和的不等式？这些环环相扣的问题构成了 Ky Fan 研究的核心议题。

## 三、主要定理与结果

Ky Fan 在 1949--1951 年间建立了三组核心结果，它们层层递进，形成了一个完整的理论体系：

### 3.1 Ky Fan 极值原理

**定理（Ky Fan, 1949/1951）**：设 $A$ 为 $n \times n$ Hermite 矩阵，特征值降序排列为 $\lambda_1 \geq \cdots \geq \lambda_n$。则

$$\sum_{i=1}^{k} \lambda_i(A) = \max_{\dim V = k} \operatorname{tr}(P_V A P_V) = \max_{\dim V = k} \sum_{j=1}^{k} \langle A v_j, v_j \rangle$$

其中 $V$ 遍历 $\mathbb{C}^n$ 的所有 $k$ 维子空间，$\{v_1, \ldots, v_k\}$ 是 $V$ 的任意标准正交基，$P_V$ 是到 $V$ 上的正交投影。

这一结果将 Courant-Fischer 定理从单个特征值推广到了特征值的部分和，赋予前 $k$ 个最大特征值之和一个清晰的变分意义：它是 Hermite 矩阵在所有 $k$ 维子空间上的"限制迹"的最大值。经典的 Courant-Fischer 定理将第 $k$ 个特征值表为一个"极大极小"问题，而 Ky Fan 的极值原理将前 $k$ 个特征值之和表为一个纯粹的"极大"问题，形式更为简洁。类似地，对最小特征值也有对偶结果：$\sum_{i=n-k+1}^{n} \lambda_i(A)$ 等于限制迹在所有 $k$ 维子空间上的最小值。

### 3.2 Ky Fan 最大特征值和不等式

**定理（Ky Fan, 1949）**：设 $A$、$B$ 为 $n \times n$ Hermite 矩阵，其特征值按降序排列。则对任意 $1 \leq k \leq n$，

$$\sum_{i=1}^{k} \lambda_i(A+B) \leq \sum_{i=1}^{k} \lambda_i(A) + \sum_{i=1}^{k} \lambda_i(B)$$

此不等式的证明是极值原理的直接推论：由于 $\sum_{i=1}^{k} \lambda_i(A+B) = \max_{\dim V = k} \operatorname{tr}(P_V (A+B) P_V) = \max_{\dim V = k} [\operatorname{tr}(P_V A P_V) + \operatorname{tr}(P_V B P_V)]$，而对固定的 $V$，$\operatorname{tr}(P_V A P_V) \leq \max_{\dim V=k} \operatorname{tr}(P_V A P_V) = \sum_{i=1}^{k} \lambda_i(A)$，对 $B$ 同理，不等式随即得证。

这一结果的边界情形值得注意。当 $k = n$ 时，两端均等于矩阵的迹 $\operatorname{tr}(A+B) = \operatorname{tr}(A) + \operatorname{tr}(B)$，等式成立。当 $k = 1$ 时，此不等式退化为 Weyl 不等式的特殊情形 $\lambda_1(A+B) \leq \lambda_1(A) + \lambda_1(B)$。因此，Ky Fan 不等式可以看作连接 $k=1$（Weyl 型）与 $k=n$（迹等式）之间的一族不等式，随着 $k$ 的增大，不等式逐渐趋向等式。

用 majorization 的语言来说，Ky Fan 不等式等价于弱 majorization 关系 $\lambda(A+B) \prec_w \lambda(A) + \lambda(B)$，即矩阵和的特征值向量被两个矩阵特征值向量之和弱控制。

### 3.3 Ky Fan 范数与控制定理

在 1951 年的论文中，Ky Fan 进一步将上述思想从 Hermite 矩阵的特征值推广到一般矩阵的奇异值，并从有限维空间推广到 Hilbert 空间上的完全连续算子（紧算子）。他引入了以其名字命名的矩阵范数：

**定义（Ky Fan $k$-范数）**：对 $n \times n$ 矩阵 $X$，其 Ky Fan $k$-范数定义为前 $k$ 个最大奇异值之和：

$$\|X\|_{(k)} = \sum_{i=1}^{k} s_i(X), \quad 1 \leq k \leq n$$

其中 $s_1(X) \geq s_2(X) \geq \cdots \geq s_n(X) \geq 0$ 为 $X$ 的奇异值，即 $X^*X$ 的特征值的非负平方根。当 $k=1$ 时，$\|X\|_{(1)} = s_1(X)$ 即谱范数（算子范数）；当 $k=n$ 时，$\|X\|_{(n)} = \sum_{i=1}^{n} s_i(X)$ 即迹范数（核范数）。Ky Fan $k$-范数在这两个极端之间提供了一族连续过渡的范数。

**Ky Fan 控制定理（Fan Dominance Theorem）**：对 $n \times n$ 矩阵 $A$ 和 $B$，以下两个条件等价：

(i) 对所有 $1 \leq k \leq n$，$\|A\|_{(k)} \leq \|B\|_{(k)}$

(ii) 对所有酉不变范数 $\||\cdot\||$，$\||A\|| \leq \||B\||$

这里，酉不变范数是指满足 $\||UAV\|| = \||A\||$ 对所有酉矩阵 $U$、$V$ 成立的矩阵范数。等价地，酉不变范数仅依赖于矩阵的奇异值，可以表示为奇异值向量上的对称规范函数（symmetric gauge function）。Ky Fan 控制定理的深刻意义在于：有限个 Ky Fan $k$-范数的比较（条件 (i)）就完全决定了无穷多个酉不变范数的比较（条件 (ii)）。Ky Fan 范数构成了酉不变范数锥的"极端射线"，在几何上它们是最"尖锐"的酉不变范数。

## 四、核心方法

Ky Fan 的证明方法融合了三种关键技术，每一种都具有独立的方法论价值：

**变分方法（Variational Method）**：核心思想是将特征值的部分和表述为一个在 Grassmann 流形（即所有 $k$ 维子空间构成的空间）上的优化问题。通过将 Rayleigh 商从单向量推广到子空间上的"限制迹"，Ky Fan 建立了特征值部分和的变分刻画。这一推广并非简单的形式化延伸：Rayleigh 商 $\langle Ax, x \rangle / \langle x, x \rangle$ 对应的是一维投影，而限制迹 $\operatorname{tr}(P_V A P_V)$ 对应的是 $k$ 维投影，后者需要对 Hermite 矩阵谱分解的精细结构进行深入分析。关键的一步是证明最大值恰好在特征子空间（即由前 $k$ 个最大特征值对应的特征向量张成的子空间）上取到。

**子空间维数论证（Dimension Counting）**：这是证明中最精妙的环节，也是后续矩阵不等式证明中被反复使用的核心技巧。关键观察在于线性代数中一个基本的维数公式：若 $V$ 和 $W$ 是 $n$ 维空间的子空间，则 $\dim(V \cap W) \geq \dim V + \dim W - n$。因此，若 $\dim V = k$ 且 $\dim W = n - k + 1$，则 $V \cap W$ 至少是一维的。Ky Fan 巧妙地将这一简单的维数计数原理与特征子空间的结构结合：通过选择 $V$ 为待优化的 $k$ 维子空间，$W$ 为与特征子空间相关的适当补空间，利用它们的非平凡交集来建立约束，最终通过在适当选择的子空间上取极值，完成了不等式的证明。这一论证技术的精髓在于，将代数不等式的证明转化为线性子空间的几何位置关系分析。

**Courant-Fischer 原理的推广**：经典的 Courant-Fischer 定理将第 $k$ 个特征值表述为

$$\lambda_k(A) = \max_{\dim V = k} \min_{x \in V, \|x\|=1} \langle Ax, x \rangle$$

Ky Fan 的关键洞察是将内层的 $\min$（在 $V$ 中取单位向量的 Rayleigh 商的最小值）替换为在 $V$ 上求迹的运算。由于 $\operatorname{tr}(P_V A P_V) = \sum_{j=1}^{k} \langle Av_j, v_j \rangle$ 是 $V$ 中标准正交基上 Rayleigh 商的**求和**而非**取最小**，这一替换将"极大极小"问题转化为纯粹的"极大"问题，不仅得到了部分和的直接刻画，还大大简化了后续不等式的推导。

这三种方法的有机结合，使得 Ky Fan 的证明既简洁又深刻，完全在经典线性代数和泛函分析的框架内完成，无需借助更高深的代数几何或表示论工具。正是这种方法上的经济性和优雅性，使得这些结果迅速成为教科书中的标准内容。

## 五、重要性与影响

Ky Fan 的矩阵不等式在多个层面产生了深远影响。

在**纯数学**层面，这些结果打通了特征值理论与矩阵范数理论之间的通道。Ky Fan 极值原理提供了一个统一的变分框架，使得此前零散的特征值不等式成为一个有机整体的特殊情形。Ky Fan 控制定理则彻底厘清了酉不变范数的结构：任何酉不变范数都可以通过奇异值上的对称规范函数（symmetric gauge function）来刻画，而 Ky Fan 范数恰好构成了这一范数族的"极端射线"。这一结构性洞察为后续的矩阵分析理论奠定了基础。von Neumann 与 Schatten 对称理想的理论、以及后来 Gohberg 和 Krein 的奇异值理论，都在不同程度上受益于 Ky Fan 的范数框架。

在**方法论**层面，Ky Fan 的子空间维数论证成为证明矩阵不等式的标准范式。这一简洁而强大的技术被后续研究者广泛采用，催生了大量新的特征值不等式和奇异值不等式。可以说，Ky Fan 的维数论证方法为"如何从变分刻画推导矩阵不等式"提供了一个通用的方法论模板，其影响力远超他本人的具体结果。

在**应用**层面，Ky Fan 范数在统计学、信号处理和优化理论中扮演着核心角色。矩阵的低秩近似问题（如 Eckart-Young 定理）可以在 Ky Fan 范数的框架下获得自然的推广和统一理解。在现代数据科学中，主成分分析（PCA）的目标恰好是最大化数据协方差矩阵在 $k$ 维子空间上的限制迹，这正是 Ky Fan 极值原理的直接体现。

仅 1949 年的第一篇论文就获得了超过 500 次引用，并持续激发着新的研究方向。1985 年，为庆祝 Ky Fan 退休，加州大学圣塔芭芭拉分校举办了一次国际数学会议，来自世界各地的数学家汇聚一堂。会议论文集《Nonlinear and Convex Analysis: Proceedings in Honor of Ky Fan》记录了他对数学多个分支的深远影响。

## 六、解决了什么瓶颈

在 Ky Fan 的工作之前，数学家所掌握的工具主要是 Weyl 不等式和 Courant-Fischer 定理，它们只能控制矩阵和的**单个**特征值。例如，Weyl 不等式告诉我们：

$$\lambda_i(A) + \lambda_j(B) \leq \lambda_{i+j-1}(A+B)$$

但如果我们想要了解"矩阵 $A+B$ 的前 $k$ 个最大特征值的总能量（总和）与 $A$、$B$ 各自前 $k$ 个最大特征值总能量的关系"，Weyl 不等式就力不从心了。简单地对 Weyl 不等式逐项求和并不能得到最优的部分和不等式，因为不同项使用不同的指标组合会导致严重的信息损失。

举一个具体的例子来说明这一困难。考虑 $3 \times 3$ Hermite 矩阵 $A$ 和 $B$，若要控制 $\lambda_1(A+B) + \lambda_2(A+B)$。使用 Weyl 不等式，我们可以分别得到 $\lambda_1(A+B) \leq \lambda_1(A) + \lambda_1(B)$ 和 $\lambda_2(A+B) \leq \lambda_2(A) + \lambda_2(B)$（取 $i=j$ 的特殊情形），相加得到 $\lambda_1(A+B) + \lambda_2(A+B) \leq [\lambda_1(A) + \lambda_2(A)] + [\lambda_1(B) + \lambda_2(B)]$。在这个特殊情形下，结果恰好与 Ky Fan 不等式一致。但对于更一般的指标选择（如 Thompson-Freede 型不等式所需的非连续指标集），逐项求和策略完全失败。Ky Fan 的方法绕过了逐项求和的策略，直接从部分和的变分刻画出发，一步到位地得到了最优不等式。

更重要的是，Ky Fan 的极值原理为部分和不等式提供了内在的变分解释，揭示了它不是 Weyl 不等式的简单推论，而是一个独立的、更深层次的结构性结果。这一变分刻画还暗示了一个更大的图景：特征值部分和满足的不等式系统远比 Weyl 型逐项不等式丰富得多，这一预感最终在 Horn 猜想中得到了完整的实现。

## 七、与前人工作的关系

Ky Fan 的工作植根于三条重要的学术传统，并在每一条传统上实现了本质性的推进：

**Weyl（1912）特征值不等式**：Hermann Weyl 在 1912 年的论文中建立了 Hermite 矩阵的逐项特征值不等式，证明了对 $i + j - 1 \leq n$ 有 $\lambda_{i+j-1}(A+B) \leq \lambda_i(A) + \lambda_j(B)$。这一结果的最初动机来自偏微分方程特征值的渐近分布和黑体辐射理论，但很快被认识到具有独立的线性代数价值。Ky Fan 1949 年第一篇论文的标题"On a Theorem of Weyl"直接表明了与 Weyl 工作的传承关系。Ky Fan 的贡献是将 Weyl 的逐项控制提升为部分和控制，实现了从"点"到"集合"的质的飞跃。值得注意的是，1949 年 Weyl 本人也在 PNAS 上发表了一篇相关论文"Inequalities between the Two Kinds of Eigenvalues of a Linear Transformation"，讨论特征值与奇异值的关系，可见这一方向在当时的活跃程度。

**Courant-Fischer 极大极小原理**：Ernst Fischer 在 1905 年率先为二次型的最小特征值建立了变分刻画，Weyl 在 1909 年将其推广到中间特征值，Courant 在 1920 年代完成了完整的统一表述。Courant-Fischer 定理将第 $k$ 个特征值表为 $\lambda_k = \max_{\dim V = k} \min_{x \in V, \|x\|=1} \langle Ax, x \rangle$。Ky Fan 的极值原理可以视为将 Courant-Fischer 定理从"一维 Rayleigh 商的极大极小"推广到"$k$ 维限制迹的极大"，但这一推广需要全新的数学洞察。事实上，Ky Fan 的极值原理逻辑上独立于 Courant-Fischer 定理--后者可以作为前者 $k=1$ 情形的推论。

**Von Neumann（1937）迹不等式**：John von Neumann 在 1937 年发表于 Tomsk 大学学报上的迹不等式 $|\operatorname{tr}(AB)| \leq \sum_i s_i(A) s_i(B)$ 将矩阵乘积的迹与奇异值联系起来，首次揭示了迹泛函与奇异值序列之间的深层联系。Ky Fan 在普林斯顿期间与 von Neumann 有密切交流，von Neumann 的迹不等式思想对 Ky Fan 发展酉不变范数理论产生了直接影响。Ky Fan 控制定理在某种意义上是 von Neumann 迹不等式思想在范数理论中的系统化延伸：von Neumann 关注的是迹（一个特定的酉不变泛函），Ky Fan 则关注所有酉不变范数构成的整个族。

## 八、对后续工作的影响

Ky Fan 的矩阵不等式催生了此后半个世纪中矩阵理论和相关领域最重要的几条研究线索：

**Horn 猜想（1962，解决于 1998--1999）**：Alfred Horn 在 1962 年发表于 Pacific Journal of Mathematics 的论文中提出了完整刻画 Hermite 矩阵和的特征值的递归不等式系统。具体地，Horn 猜想断言：给定三组实数 $\alpha$、$\beta$、$\gamma$，存在特征值分别为 $\alpha$、$\beta$、$\gamma$ 的 $n \times n$ Hermite 矩阵 $A$、$B$、$C$ 使得 $A + B = C$，当且仅当 $\sum \alpha_i + \sum \beta_i = \sum \gamma_i$ 且对所有属于递归定义的指标集 $T_r^n$ 的三元组 $(I, J, K)$ 均满足 $\sum_{i \in I} \gamma_i \leq \sum_{i \in I} \alpha_i + \sum_{j \in J} \beta_j$。Ky Fan 不等式对应于最简单的情形 $I = J = K = \{1, 2, \ldots, k\}$。这一猜想最终由 Alexander Klyachko（1998，通过几何不变量理论和稳定向量丛理论）和 Allen Knutson 与 Terence Tao（1999，通过"蜂巢"组合模型证明饱和猜想）联合解决。这一成就将矩阵特征值不等式与 Schubert 计算、Grassmann 流形的上同调、表示论等领域深刻地联系在一起，被视为 20 世纪末数学中最美丽的交叉成果之一。

**Lidskii 不等式与 majorization**：V. B. Lidskii 在 1950 年建立的特征值扰动不等式可以用 majorization 关系表述为 $\lambda(A) - \lambda(B) \prec \lambda(A-B)$。Lidskii-Mirsky-Wielandt 定理进一步将这些结果统一到 majorization 理论的框架中。Li 和 Mathias 在 1999 年给出了该定理的加法和乘法两个版本的统一证明。Lewis 则在 1999 年用非光滑分析的方法给出了 Lidskii 定理的新证明，揭示了特征值不等式与优化理论之间的深层联系。

**Thompson-Freede 定理（1971）**：R. C. Thompson 和 L. J. Freede 将 Ky Fan 类型的不等式推广到对选定指标子集（而非连续的前 $k$ 个）的特征值部分和，建立了更精细的约束条件。这一工作预示了 Horn 猜想的完整形式。

**Majorization 理论的系统发展**：Ky Fan 的部分和不等式本质上是一个弱 majorization 关系。这一观察推动了 majorization 理论在矩阵分析中的系统应用。Marshall 和 Olkin 的经典著作《Inequalities: Theory of Majorization and Its Applications》（1979，第二版 2011 年与 Arnold 合著）将 majorization 和 Schur-convexity 发展为一个完整的理论框架，Ky Fan 不等式是其中的核心素材之一。

## 九、现代价值

Ky Fan 的矩阵不等式在当代科学和工程中继续发挥着深远作用：

**量子信息理论**：在量子计算和量子通信中，密度矩阵的特征值描述了量子态的谱特性。Ky Fan 不等式和 majorization 关系被用于刻画量子纠缠的度量、量子信道的容量以及量子态转换的可能性。特别是，Nielsen 在 1999 年证明了纯态纠缠转换的充要条件恰好由 majorization 关系给出，而 majorization 的验证正是通过检验 Ky Fan 型部分和不等式来实现的。von Neumann 熵的次可加性和连续性界限也在本质上依赖于 Ky Fan 类型的特征值控制。2025 年，Czartowski 等人进一步将 Ky Fan 的 majorization 关系推广到可分算子的张量积设定，利用线性规划方法精炼了相应的特征值和上界。

**随机矩阵理论**：在 Wigner 矩阵和 Wishart 矩阵的研究中，特征值部分和的极限分布是核心对象之一。Ky Fan 的极值原理为理解这些分布提供了确定性的上下界。Tracy-Widom 分布描述了最大特征值的涨落，而前 $k$ 个特征值之和的联合分布则需要 Ky Fan 极值原理的多维推广。

**优化理论与机器学习**：矩阵的核范数（即 Ky Fan $n$-范数）松弛已成为低秩矩阵恢复和矩阵补全问题的标准方法。在推荐系统（如 Netflix 竞赛）、图像修复、协同过滤等应用中，核范数最小化被用作秩最小化的凸松弛。其理论基础正可追溯到 Ky Fan 对奇异值部分和与酉不变范数关系的刻画。此外，Ky Fan $k$-范数本身也被用作正则化项，在希望控制矩阵前 $k$ 个奇异值（而非全部）时特别有用。

**信号处理与通信**：在多输入多输出（MIMO）通信系统中，信道矩阵的奇异值决定了各子信道的通信容量。Ky Fan 范数为分析信道容量的部分和提供了自然的数学框架。在阵列信号处理中，MUSIC 和 ESPRIT 等谱估计算法的性能分析也涉及特征值部分和的精确控制。

## 十、通俗解读

想象一个公司有 $n$ 个部门，每个部门的"产出能力"由一个数值衡量--这就是矩阵的特征值。矩阵 $A$ 代表公司甲的各部门产出能力，矩阵 $B$ 代表公司乙的各部门产出能力。当两家公司合并时，合并后公司各部门的产出能力由矩阵 $A+B$ 的特征值描述。

Weyl 不等式告诉我们一个"局部"规律：合并后最强的单个部门，不会比甲的最强部门和乙的最强部门的能力简单相加更强。这是一种逐项的控制。

Ky Fan 不等式则告诉我们一个更强的"整体"规律：合并后**最强的 $k$ 个部门的总产出**，不会超过甲的最强 $k$ 个部门的总产出加上乙的最强 $k$ 个部门的总产出。换句话说，不存在一种"协同效应"能让合并后的前 $k$ 名变得比两家公司各自前 $k$ 名简单相加更强。最优方向上的资源整合满足次可加性。

这个"部分和控制"比"逐项控制"强得多。打个比方：如果我们只知道考试中每道题的最高可能得分，我们对总分能说的很有限；但如果我们知道"前 $k$ 道最高分之和"的上界（对所有 $k$ 同时成立），我们就几乎完全掌握了总分的分布规律。

Ky Fan 极值原理的直觉则更为有趣：它说的是，前 $k$ 个最大特征值之和等于"最优 $k$ 维观察窗口"下所看到的总效果。如果你有一副只能同时看 $k$ 个方向的"眼镜"，那么无论你怎么调整这副眼镜的朝向，你看到的总效果都不会超过前 $k$ 个特征值之和；而如果你恰好对准了前 $k$ 个特征方向，你就看到了最大的总效果。

## 十一、阅读指南

对于有志于深入学习 Ky Fan 矩阵不等式的读者，建议按照以下路径循序渐进：

**第一阶段（本科高年级）**：从 Roger A. Horn 和 Charles R. Johnson 的《Matrix Analysis》（第二版，Cambridge University Press, 2013）第 4 章开始，该章系统介绍了 Hermite 矩阵的特征值不等式，包括 Ky Fan 不等式的现代证明。本书以严谨而清晰的风格著称，是线性代数和矩阵理论的标准教科书。

**第二阶段（研究生）**：Rajendra Bhatia 的《Matrix Analysis》（Springer, 1997）第 III 章（majorization 与双随机矩阵）和第 IV 章（酉不变范数与 Ky Fan 控制定理）提供了更深入的理论讨论，将 Ky Fan 不等式置于 majorization 和对称函数理论的更广阔框架中。

**第三阶段（研究视角）**：Terence Tao 的博客文章"254A, Notes 3a: Eigenvalues and sums of Hermitian matrices"以现代视角重新审视了从 Weyl 不等式到 Horn 猜想的整条发展线索，是了解 Ky Fan 不等式在特征值问题全貌中位置的绝佳资源。Fulton 的综述"Eigenvalues, Invariant Factors, Highest Weights, and Schubert Calculus"则将读者引向代数几何与表示论的方向。

**原始文献**：Ky Fan 的三篇 PNAS 论文篇幅简短（总共不超过 20 页），文风清晰凝练，对于具备线性代数和实分析基础的读者而言完全可以直接阅读。建议按时间顺序阅读 1949（I）、1950（II）、1951 三篇，体会思想的逐步深化。这些论文可在 PNAS 官方网站和 PubMed Central 免费获取。

## 十二、局限性

Ky Fan 的矩阵不等式主要针对 Hermite（自伴）矩阵或正规矩阵建立，其向非正规矩阵的推广面临本质困难。对于非正规矩阵，特征值不再具有实性和正交特征子空间等良好性质，变分方法失去了直接适用性。虽然 Ky Fan 在 1951 年论文中讨论了一般矩阵特征值的实部与奇异值之间的 majorization 关系（后来由 Amir-Moez、Horn 和 Mirsky 独立证明了其逆），但这些结果的形式不如 Hermite 情形那么简洁和完整。

其次，Ky Fan 不等式给出的是**必要条件**而非充分条件。即便 $A$ 和 $B$ 的特征值满足所有 Ky Fan 不等式，也不能保证存在具有这些特征值的 Hermite 矩阵 $C = A + B$。特征值可行域的完整刻画远比 Ky Fan 不等式所描述的复杂得多，其最终的充要条件由 Horn 猜想给出，解决这一猜想需要 Schubert 计算、量子上同调和几何不变量理论等远为深奥的工具。

Ky Fan 的原始工作也主要限于有限维空间和紧算子。虽然他在 1951 年的论文中已经将结果推广到 Hilbert 空间上的完全连续算子，但向更一般的无界自伴算子或非紧算子的推广涉及谱理论中连续谱和本征谱交互的微妙技术问题，至今仍是活跃的研究方向。

最后，从应用角度看，Ky Fan 不等式作为上界往往不够紧致。在许多具体问题中，实际的特征值关系远比 Ky Fan 不等式所允许的更受限。更精细的约束需要用到 Thompson-Freede 型不等式乃至 Horn 系统的完整递归结构。

## 十三、延伸阅读

1. **R. Bhatia**, *Matrix Analysis*, Springer Graduate Texts in Mathematics, Vol. 169, 1997. --矩阵分析的权威教科书，系统讨论了 Ky Fan 不等式和 majorization 理论。

2. **A. W. Marshall, I. Olkin, B. C. Arnold**, *Inequalities: Theory of Majorization and Its Applications*, 2nd ed., Springer, 2011. --majorization 理论的百科全书式参考。

3. **A. Knutson, T. Tao**, "Honeycombs and Sums of Hermitian Matrices," *Notices of the AMS*, 48(2), 175--186, 2001. --对 Horn 猜想解决过程的精彩综述。

4. **R. Bhatia**, "Linear Algebra to Quantum Cohomology: The Story of Alfred Horn's Inequalities," *American Mathematical Monthly*, 108(4), 289--318, 2001. --从 Ky Fan 不等式到 Horn 猜想的历史综述。

5. **W. Fulton**, "Eigenvalues, Invariant Factors, Highest Weights, and Schubert Calculus," *Bulletin of the AMS*, 37(3), 209--249, 2000. --将特征值不等式与代数几何联系起来的深度综述。

6. **M. S. Moslehian**, "Ky Fan Inequalities," *Linear and Multilinear Algebra*, 60(11--12), 1313--1325, 2012. --对各类以 Ky Fan 命名的不等式的系统梳理。

7. **S. Kapovich**, "A Survey of the Additive Eigenvalue Problem," *Transformation Groups*, 19, 1051--1148, 2014. --加法特征值问题的现代综述，涵盖从 Ky Fan 到 Horn 猜想的完整发展。

8. **T. Tao**, "254A, Notes 3a: Eigenvalues and Sums of Hermitian Matrices," *What's New* (blog), 2010. --对整个特征值和问题的现代视角梳理。

## 十四、参考文献

1. Fan, K. "On a Theorem of Weyl Concerning Eigenvalues of Linear Transformations I." *Proc. Natl. Acad. Sci. U.S.A.* **35**(11): 652--655, 1949. DOI: 10.1073/pnas.35.11.652

2. Fan, K. "On a Theorem of Weyl Concerning Eigenvalues of Linear Transformations II." *Proc. Natl. Acad. Sci. U.S.A.* **36**(1): 31--35, 1950. DOI: 10.1073/pnas.36.1.31

3. Fan, K. "Maximum Properties and Inequalities for the Eigenvalues of Completely Continuous Operators." *Proc. Natl. Acad. Sci. U.S.A.* **37**(11): 760--766, 1951. DOI: 10.1073/pnas.37.11.760

4. Weyl, H. "Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen." *Math. Ann.* **71**: 441--479, 1912. DOI: 10.1007/BF01456804

5. von Neumann, J. "Some Matrix-Inequalities and Metrization of Matric-Space." *Tomsk Univ. Rev.* **1**: 286--300, 1937.

6. Horn, A. "Eigenvalues of Sums of Hermitian Matrices." *Pacific J. Math.* **12**: 225--241, 1962.

7. Klyachko, A. A. "Stable Vector Bundles and Hermitian Operators." *Selecta Math. (N.S.)* **4**: 419--445, 1998.

8. Knutson, A. and Tao, T. "The Honeycomb Model of GL_n(C) Tensor Products I: Proof of the Saturation Conjecture." *J. Amer. Math. Soc.* **12**: 1055--1090, 1999.

9. Thompson, R. C. and Freede, L. J. "On the Eigenvalues of Sums of Hermitian Matrices." *Linear Algebra Appl.* **4**: 369--376, 1971.

10. Fan, K. "Inequalities for Eigenvalues of Hermitian Matrices." *Contributions to the Solution of Systems of Linear Equations and the Determination of Eigenvalues*, NBS Applied Mathematics Series No. 39, 131--139, 1954.

11. Mirsky, L. "A Trace Inequality of John von Neumann." *Monatshefte fur Mathematik* **79**: 303--306, 1975.

12. Lidskii, V. B. "On the Eigenvalues of the Sum and Product of Symmetric Matrices." *Doklady Akad. Nauk SSSR* **75**: 769--772, 1950.

---

*本文写作参考了 PNAS 原始论文、Bhatia 的 Matrix Analysis、Tao 的博客笔记、Moslehian 的综述文献以及 Fulton 的 Bulletin of the AMS 综述。文中数学表述遵循现代矩阵分析的标准记法。*
