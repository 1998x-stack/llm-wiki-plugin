# Schur酉三角化定理：矩阵分解理论的基石

## 作者

**Issai Schur（伊赛·舒尔，1875--1941）**

俄裔德国数学家，柏林大学教授，20世纪代数学与矩阵理论的核心奠基人之一。Schur 于1875年1月10日出生于俄罗斯帝国莫吉廖夫（今白俄罗斯境内），13岁移居拉脱维亚利耶帕亚，在当地德语文法学校接受教育并以金质奖章毕业。1894年入柏林大学攻读数学与物理，师从 Frobenius，1901年以一般线性群的有理表示理论获博士学位。1903年起任柏林大学讲师，1911--1916年任波恩大学教授，1919年回柏林大学任正教授，1922年当选普鲁士科学院院士。Schur 的研究横跨群表示论、矩阵理论、数论、积分方程论与函数论，以其名字命名的数学概念多达二十余项。1935年被纳粹政权强制退休，1939年流亡巴勒斯坦，1941年1月10日——恰逢66岁生日——因心脏病发于特拉维夫逝世。

## 发表时间与出处

**1909年**，发表于 *Mathematische Annalen*，第66卷，第488--510页。

论文原题为德文：*"Über die charakteristischen Wurzeln einer linearen Substitution mit einer Anwendung auf die Theorie der Integralgleichungen"*（《论线性代换的特征根及其在积分方程理论中的一个应用》）。该文发表于由 Felix Klein 与 David Hilbert 主编的 *Mathematische Annalen*——当时欧洲最具影响力的数学期刊之一。论文共23页，结构紧凑而内容深远，包含了酉三角化定理、Schur不等式以及正规矩阵的对角化判据三项核心成果。

## 一句话概括

任意复数域上的方阵均可通过酉相似变换化为上三角阵——即对任意 $A \in \mathbb{C}^{n \times n}$，存在酉矩阵 $Q$ 使得 $A = QTQ^*$，其中 $T$ 为上三角矩阵且对角元素恰为 $A$ 的全部特征值——这一定理以最简洁的形式揭示了矩阵的谱结构，并为现代数值线性代数奠定了理论基石。

## 历史背景与动机

Schur 发表酉三角化定理的1909年，正值矩阵理论与算子理论经历深刻变革的时期。要理解这一定理的诞生，需要将目光投向19世纪中叶以来线性代数的演进脉络，以及20世纪初柏林与哥廷根两大数学学派的学术生态。

矩阵的标准形问题是19世纪代数学的核心议题。1870年，Camille Jordan 在其巨著《代换与代数方程论》中系统建立了 Jordan 标准形理论，证明了每个方阵在代数闭域上相似于一个由 Jordan 块组成的准对角矩阵。此后，Karl Weierstrass（1868）与 Leopold Kronecker（1874）从双线性型的分类角度发展了初等因子理论，为矩阵的相似分类提供了更精细的不变量。Ferdinand Georg Frobenius——Schur 的博士导师——于1878--1879年间发表了关于有理标准形（Frobenius标准形）的奠基性工作，建立了不依赖于域扩张的矩阵分类框架。Schur 在柏林大学深受 Frobenius 的影响，对矩阵代数的结构理论有着深厚的根基。

然而，Jordan 标准形虽在理论上完美，却存在一个根本性的缺陷：它对矩阵元素的微小扰动极为敏感。当矩阵的特征值具有高重数时，Jordan 块的结构可能因微小的数值误差而发生剧烈改变——一个具有 $k$ 阶 Jordan 块的矩阵，在任意小的扰动下可能分裂为 $k$ 个不同的简单特征值。这种数值不稳定性意味着 Jordan 标准形虽是相似分类的最终答案，却无法直接服务于实际计算。

与此同时，David Hilbert 在哥廷根开创了积分方程的谱理论。1904--1910年间，Hilbert 在哥廷根科学院通讯中连续发表六篇关于线性积分方程的通讯，后汇编为专著《线性积分方程一般理论纲要》（1912）。Hilbert 将有限维线性代数的特征值理论推广到无穷维函数空间，引入了"谱"（Spektrum）的概念——这个源自物理学的术语日后成为泛函分析的核心范畴。Hilbert 的学生 Erhard Schmidt（1905--1907）进一步将对称核的理论扩展到非对称情形，发展了奇异值理论的雏形。

正是在这一背景下，Schur——既是 Frobenius 在柏林的学术传人，又与哥廷根的 Hilbert 学派保持着密切的学术联系——着手研究一个介于 Jordan 标准形与积分方程谱理论之间的问题：能否找到一种既能揭示特征值信息、又保持变换矩阵良好数值性质的矩阵分解？他的回答是肯定的：通过酉（正交）变换将任意方阵化为上三角形式。酉矩阵保范、保内积的性质确保了这一分解的数值稳定性，而上三角形式的对角元素直接给出全部特征值——这一结果以优雅的方式兼顾了理论的完整性与计算的可靠性。

此外，Schur 论文的副标题"在积分方程理论中的一个应用"明确表明，他的动机并非纯粹的矩阵代数。他将有限维的酉三角化结果应用于积分方程的核函数，为 Hilbert-Schmidt 理论提供了新的证明路径。这种将有限维技术向无穷维推广的方法论，成为20世纪算子理论发展的重要范式。

值得注意的是，1909年前后正是线性代数从"方程组求解工具"向"抽象结构理论"转型的关键时期。Arthur Cayley（1858）引入矩阵概念时，矩阵仅被视为线性方程组的简写；而到了 Schur 的时代，矩阵已被视为独立的代数对象，其内在结构——特征值、不变子空间、标准形——成为研究的核心。Schur 的酉三角化定理恰好站在这一转型的枢纽位置：它既回应了经典标准形理论的核心问题，又以其对酉变换的强调预示了泛函分析时代的到来。在柏林大学的讲堂上，Schur 吸引了数百名学生——据记载，1930年冬季学期他的数论课程甚至超出了拥有五百个座位的第二大阶梯教室的容量——这位学者对数学教育的热忱与其理论贡献同样令人景仰。

## 核心问题

**如何将任意方阵化为最简形式，同时保持变换的数值稳定性？**

更精确地说，Schur 所面对的核心问题可以分解为以下层次：

（一）**理论层面**：Jordan 标准形已经给出了矩阵在相似变换下的最细分类，但相似变换 $P^{-1}AP$ 中的变换矩阵 $P$ 可能具有极大的条件数，使得从 $A$ 到 Jordan 形的映射在拓扑上不连续。能否在限制变换矩阵类别（如要求正交/酉性）的条件下，仍然获得尽可能简单的标准形？

（二）**计算层面**：在实际计算中，矩阵元素总是带有舍入误差。理想的矩阵分解应当对微小扰动保持稳定——即输入矩阵的微小变化只引起输出的微小变化。酉变换 $Q^*AQ$ 由于 $\|Q\|_2 = 1$，天然满足此要求。

（三）**谱信息提取**：分解后的形式应当直接展现矩阵的特征值信息，无需额外的计算步骤。上三角矩阵的特征值恰为其对角元素，因此 Schur 分解完美满足此需求。

## 主要定理与结果

Schur 在1909年的论文中建立了三项紧密关联的核心结果：

### 定理一：Schur酉三角化定理（Schur Decomposition）

设 $A \in \mathbb{C}^{n \times n}$ 为任意 $n$ 阶复方阵。则存在酉矩阵 $Q \in \mathbb{C}^{n \times n}$（满足 $Q^*Q = QQ^* = I$）和上三角矩阵 $T \in \mathbb{C}^{n \times n}$，使得

$$A = QTQ^*$$

其中 $T$ 的对角元素 $t_{11}, t_{22}, \ldots, t_{nn}$ 恰为 $A$ 的全部特征值 $\lambda_1, \lambda_2, \ldots, \lambda_n$（按某一排列，计重数）。

等价地，存在 $\mathbb{C}^n$ 的一组标准正交基 $\{q_1, q_2, \ldots, q_n\}$，使得 $A$ 在此基下的矩阵表示为上三角形式。这等价于存在一个由 $A$-不变子空间构成的完全旗（complete flag）：

$$\{0\} = V_0 \subset V_1 \subset V_2 \subset \cdots \subset V_n = \mathbb{C}^n$$

其中 $\dim V_k = k$，每个 $V_k$ 均为 $A$-不变子空间，且前 $k$ 个基向量 $q_1, \ldots, q_k$ 构成 $V_k$ 的标准正交基。

需要指出，Schur 分解一般不唯一：特征值在对角线上的排列顺序可以任意选取，且当存在重特征值时，酉矩阵 $Q$ 的选择自由度更大。

### 定理二：Schur不等式

设 $A = (a_{ij}) \in \mathbb{C}^{n \times n}$ 的特征值为 $\lambda_1, \lambda_2, \ldots, \lambda_n$，则

$$\sum_{i=1}^{n} |\lambda_i|^2 \leq \sum_{i=1}^{n}\sum_{j=1}^{n} |a_{ij}|^2 = \operatorname{tr}(A^*A) = \|A\|_F^2$$

其中 $\|A\|_F$ 为 $A$ 的 Frobenius 范数（亦称 Hilbert-Schmidt 范数）。等号成立当且仅当 $A$ 为正规矩阵（即 $A^*A = AA^*$）。

这一不等式的证明直接源于酉三角化：由 $A = QTQ^*$ 可知 $\|A\|_F = \|T\|_F$（酉变换保Frobenius范数），而 $\|T\|_F^2 = \sum_i |t_{ii}|^2 + \sum_{i<j} |t_{ij}|^2 \geq \sum_i |\lambda_i|^2$，等号成立当且仅当 $T$ 的严格上三角部分为零，即 $T$ 为对角阵。

### 定理三：正规矩阵的酉对角化

矩阵 $A \in \mathbb{C}^{n \times n}$ 为正规矩阵（$A^*A = AA^*$）当且仅当 $A$ 可酉对角化，即存在酉矩阵 $Q$ 和对角矩阵 $D$ 使得 $A = QDQ^*$。

这一结果是酉三角化定理与 Schur 不等式的直接推论：正规矩阵的 Schur 三角形式 $T$ 必须满足 $T^*T = TT^*$，由此可推出 $T$ 的严格上三角元素全部为零，即 $T$ 退化为对角矩阵。该定理统一了 Hermite 矩阵（实特征值）、酉矩阵（模为1的特征值）和反 Hermite 矩阵（纯虚特征值）的谱分解。

## 核心方法与证明思路

Schur 的证明方法以简洁著称，核心工具是数学归纳法与正交化过程。以下为证明的现代表述。

**基始步骤**：当 $n = 1$ 时，$A = (\lambda_1)$ 本身即为上三角矩阵（亦为对角矩阵），取 $Q = (1)$ 即可。命题平凡成立。

**归纳假设**：设对所有 $(n-1)$ 阶复方阵，酉三角化定理成立。

**归纳步骤**：设 $A \in \mathbb{C}^{n \times n}$。由代数基本定理，$A$ 至少有一个特征值 $\lambda_1$，设 $v_1$ 为对应的单位特征向量（$\|v_1\| = 1$）。将 $v_1$ 扩充为 $\mathbb{C}^n$ 的标准正交基 $\{v_1, v_2, \ldots, v_n\}$（可通过 Gram-Schmidt 正交化完成），令酉矩阵 $U_1 = [v_1 \mid v_2 \mid \cdots \mid v_n]$。则

$$U_1^* A U_1 = \begin{pmatrix} \lambda_1 & b^* \\ 0 & A' \end{pmatrix}$$

其中 $b^* \in \mathbb{C}^{1 \times (n-1)}$ 为某行向量，$A' \in \mathbb{C}^{(n-1) \times (n-1)}$。第一列中 $\lambda_1$ 以下全为零，是因为 $Av_1 = \lambda_1 v_1$ 且 $v_2, \ldots, v_n$ 与 $v_1$ 正交。

由归纳假设，存在 $(n-1)$ 阶酉矩阵 $\hat{Q}$ 使得 $\hat{Q}^* A' \hat{Q} = T'$ 为上三角矩阵。令

$$U_2 = \begin{pmatrix} 1 & 0 \\ 0 & \hat{Q} \end{pmatrix}$$

则 $U_2$ 为 $n$ 阶酉矩阵，且

$$U_2^* (U_1^* A U_1) U_2 = \begin{pmatrix} \lambda_1 & b^* \hat{Q} \\ 0 & T' \end{pmatrix} = T$$

为上三角矩阵。令 $Q = U_1 U_2$（酉矩阵之积仍为酉矩阵），则 $Q^* A Q = T$，即 $A = QTQ^*$。证毕。

这一证明的精髓在于：每一步归纳都提取一个特征向量，通过正交补将问题的维数降低一维，直至归结为平凡情形。整个过程仅依赖两个基本事实——代数基本定理（保证特征值存在）和 Gram-Schmidt 正交化（保证正交补的构造），不需要 Jordan 理论中精细的根子空间分析。

## 重要性与地位

Schur 酉三角化定理的重要性体现在多个维度：

**理论维度**：它是矩阵谱理论中最基本的存在性定理之一。与 Jordan 标准形相比，Schur 分解虽未给出最精细的相似不变量，但它在酉等价类中提供了一种"次优但更实用"的标准形式。谱定理（正规矩阵的酉对角化）是 Schur 定理的直接推论，而非相反——这一逻辑关系常被教科书忽略。

**方法论维度**：Schur 的归纳证明为矩阵分解理论提供了一种范式：通过逐步提取特征向量并利用正交补进行降维，这一思想后来被广泛应用于 QR 分解、Hessenberg 化简、双对角化等一系列矩阵分解的构造中。

**数值维度**：酉变换保范数、保内积、条件数恒为1——这些性质使得基于酉变换的算法天然具有数值稳定性。Schur 定理从理论上保证了"通过酉变换提取全部特征值"这一目标的可行性，为半个世纪后 QR 算法的发明提供了理论依据。

**统一性维度**：正规矩阵（Hermite、酉、反Hermite等）的谱分解、非正规矩阵的特征值定位（通过 Schur 不等式）、矩阵函数的定义（通过 Schur 形式）——这些看似不同的问题都可以在 Schur 分解的统一框架下得到处理。

在现代数学教育中，Schur 分解通常在本科高等代数或研究生矩阵分析课程中讲授，被视为连接抽象代数理论与数值计算实践的关键桥梁。Gene Golub 与 Charles Van Loan 在经典教材 *Matrix Computations* 中称其为"矩阵计算中最有用的分解之一"。

## 解决了什么瓶颈

Schur 定理的核心贡献在于为 Jordan 标准形的数值不稳定性提供了一个优雅的替代方案。

**Jordan 标准形的困境**：考虑矩阵

$$J = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$$

这是一个2阶的 Jordan 块，特征值为 $\lambda = 0$（二重）。但对于扰动矩阵

$$J_\varepsilon = \begin{pmatrix} 0 & 1 \\ \varepsilon & 0 \end{pmatrix}$$

其特征值变为 $\pm\sqrt{\varepsilon}$。当 $\varepsilon = 10^{-16}$（典型的双精度舍入误差量级）时，特征值变为 $\pm 10^{-8}$——相对于矩阵元素的扰动量级 $10^{-16}$，特征值的变化被放大了 $10^8$ 倍。更严重的是，$J_\varepsilon$ 的 Jordan 形式从一个2阶块变为两个1阶块，即 Jordan 结构本身发生了不连续的跳变。

**Schur 分解的解答**：Schur 分解 $A = QTQ^*$ 对扰动的响应是连续的。具体地，若 $\tilde{A} = A + E$ 为 $A$ 的扰动，则 $\tilde{A}$ 的 Schur 形式 $\tilde{T}$ 满足 $\|\tilde{T} - T\|_F = \|E\|_F$（因为酉变换保 Frobenius 范数）。虽然酉矩阵 $Q$ 可能变化较大（当特征值接近时），但三角因子 $T$ 的变化始终受控。

**特征值定位的新工具**：Schur 不等式 $\sum |\lambda_i|^2 \leq \|A\|_F^2$ 以及由此衍生的 Schur 上界，为特征值的定位提供了无需求解特征方程的快速估计。这在大规模矩阵问题中尤为重要，因为直接求解 $n$ 次特征多项式在 $n > 4$ 时一般不可能（Abel-Ruffini 定理）。

**正规性的刻画**：Schur 不等式中等号成立的条件——$A$ 为正规矩阵——提供了判别正规性的一个计算友好的准则：只需比较 $\sum |\lambda_i|^2$ 与 $\|A\|_F^2$ 即可，无需验证 $A^*A = AA^*$ 的 $n^2$ 个等式。

## 与前人工作的关系

Schur 的酉三角化定理并非凭空而来，它深植于19世纪矩阵理论与20世纪初积分方程理论的沃土之中。

**Jordan 标准形（1870）**：Camille Jordan 建立的标准形理论是矩阵相似分类的最终答案，但它要求在代数闭域上工作，且变换矩阵的选择不受范数约束。Schur 定理可视为 Jordan 理论在"酉等价"这一更强条件下的最优结果：放弃 Jordan 形式的块对角结构（无法在酉约束下保持），换取上三角形式与酉变换矩阵。

**Frobenius 的有理标准形（1878--1879）**：Frobenius 标准形的优势在于它不依赖于域扩张——即使在实数域上也能定义。Schur 分解则走向另一个极端：它要求在复数域上工作（因为需要特征值的存在性），但通过限制变换矩阵为酉矩阵，获得了优越的数值性质。对于实矩阵，实 Schur 形式将复特征值对对应的 $2 \times 2$ 块保留在准上三角结构中。

**Hilbert 的积分方程理论（1904--1910）**：Schur 论文的标题明确指出其与积分方程理论的联系。Hilbert 在处理对称核的积分方程时，本质上建立了自伴算子的谱定理——这是正规矩阵酉对角化在无穷维空间的推广。Schur 从有限维角度提供了一条更为初等的证明路径：先证酉三角化，再由正规性推出对角化。这一思路后来被 von Neumann 等人在建立 Hilbert 空间算子理论时所继承。

**Erhard Schmidt 的奇异值理论（1907）**：Schmidt 在研究非对称核时引入的奇异值分解（SVD）与 Schur 分解有着深刻的联系。对于任意矩阵 $A$，其奇异值是 $A^*A$（正规矩阵）的特征值的正平方根。Schur 的正规矩阵对角化定理保证了 $A^*A$ 可酉对角化，从而为 SVD 的存在性提供了理论保障。

## 后续影响与衍生

Schur 1909年定理的影响远超其诞生时的历史语境，深刻地塑造了20世纪数值线性代数、矩阵分析与控制理论的发展路径。

### QR 算法（1961）

Schur 分解最重要的算法化身是 QR 算法。1959--1961年间，英国工程师 John G. F. Francis 与苏联数学家 Vera N. Kublanovskaya 独立发明了这一迭代算法。Francis 在其1961年发表于 *The Computer Journal* 的论文中明确指出，QR 算法的目标是计算矩阵的"Schur标准形"。算法的核心思想是：反复对矩阵进行 QR 分解（$A_k = Q_k R_k$），然后以相反顺序重组（$A_{k+1} = R_k Q_k = Q_k^* A_k Q_k$），使序列 $\{A_k\}$ 收敛到上三角形式——即 Schur 分解中的 $T$。QR 算法被列为"20世纪十大最有影响力的算法"之一，至今仍是 LAPACK、MATLAB 等主流数值计算软件的核心引擎。从 Schur 1909年的存在性定理到 Francis-Kublanovskaya 1961年的构造性算法，历经半个世纪的理论酝酿终于转化为计算实践。

### Schur 补（1968年命名）

虽然 Schur 补的核心思想可追溯至 Laplace（1812）与 Sylvester（1852），但其现代命名由 Emilie Haynsworth 于1968年确定，以纪念 Schur 在矩阵分块理论中的贡献。对于分块矩阵

$$M = \begin{pmatrix} A & B \\ C & D \end{pmatrix}$$

当 $D$ 可逆时，$D$ 的 Schur 补定义为 $M/D = A - BD^{-1}C$。Schur 补在高斯消元、正定性判别、统计学中的条件分布、电网络的 Kron 约化等领域具有广泛应用。Springer 出版社于2005年出版了专著 *The Schur Complement and Its Applications*，系统总结了这一概念在数学各分支中的渗透。

### 矩阵函数理论

Schur 分解为矩阵函数的定义和计算提供了标准框架。对于解析函数 $f$，矩阵函数 $f(A)$ 可通过 Schur 形式定义：若 $A = QTQ^*$，则 $f(A) = Qf(T)Q^*$，其中上三角矩阵的函数值 $f(T)$ 可通过 Parlett 递推公式高效计算。这一方法避免了 Jordan 形式中因 Jordan 块大小不同而需要导数计算的复杂性。Nicholas Higham 在其专著 *Functions of Matrices*（2008）中将 Schur-Parlett 算法作为计算矩阵函数的核心方法。

### 同时三角化

Schur 定理的一个重要推广是交换矩阵族的同时三角化：若 $\{A_1, A_2, \ldots, A_k\}$ 为一族两两交换的方阵，则存在单一的酉矩阵 $Q$，使得所有 $Q^*A_iQ$ 同时为上三角形式。这一结果在李代数的表示论与量子力学的可观测量理论中具有重要意义。

## 现代价值与应用

Schur 分解在当代科学与工程中的应用已远远超出纯数学的范畴。

**数值特征值计算**：几乎所有现代特征值求解器的底层都基于计算矩阵的（实或复）Schur 形式。LAPACK 库中的 `xGEES` 系列子程序直接计算 Schur 分解；MATLAB 的 `schur()` 函数和 Python NumPy/SciPy 中的 `scipy.linalg.schur()` 函数均提供 Schur 分解的标准接口。在大规模稀疏矩阵问题中，Krylov 子空间方法（如 Arnoldi 算法）本质上是在低维投影空间中计算部分 Schur 分解。

**控制理论**：在线性系统 $\dot{x} = Ax + Bu$ 的分析中，系统矩阵 $A$ 的 Schur 形式直接揭示系统的稳定性（特征值实部的符号）、可控性与可观性。Schur 分解还在 Riccati 方程求解、$H_\infty$ 控制设计与模型降阶中扮演核心角色。

**量子信息与量子计算**：在量子力学中，密度矩阵的谱分解（正规矩阵的 Schur 对角化）是量子态表示的基础。非正规算子的 Schur 分解则出现在开放量子系统的 Lindblad 方程分析中。

**机器学习与数据科学**：主成分分析（PCA）的数学基础是协方差矩阵的谱分解，而谱分解是 Schur 分解的特例。在谱聚类、图神经网络等现代方法中，Laplacian 矩阵的特征分解——本质上仍是 Schur 理论的应用——已成为标准工具。

**随机矩阵理论**：Schur 不等式在随机矩阵的矩估计中提供了基本的不等式工具。Wigner 半圆律、Marchenko-Pastur 律等随机矩阵理论的核心结果，其证明过程中频繁使用特征值与矩阵元素之间的迹不等式，而这些不等式的原型正是 Schur 1909年的结果。

**微分方程数值解**：在求解大规模常微分方程组 $\dot{x} = Ax$ 时，矩阵指数 $e^{At}$ 的计算可通过 Schur 分解高效实现：先计算 $A = QTQ^*$，然后 $e^{At} = Qe^{Tt}Q^*$，而上三角矩阵的指数可通过对角元素（标量指数）与严格上三角部分（有限级幂零矩阵）的组合快速求得。Cleve Moler 与 Charles Van Loan 在其经典综述"Nineteen Dubious Ways to Compute the Exponential of a Matrix"（1978, 2003）中将 Schur 方法列为最可靠的矩阵指数计算途径之一。

## 通俗化解释

想象你面对一间杂乱无章的图书馆，书籍（矩阵的列向量）随意堆放，彼此之间的关系错综复杂。Schur 定理告诉你：无论这间图书馆多么混乱，你总能找到一种"旋转书架"的方式（酉变换），使得整理之后，每一本书只与编号在它之后的书发生关联（上三角结构），而每本书的"核心标签"（特征值）都清晰地标注在书脊上（对角元素）。

更直观地说，如果把矩阵想象成一台复杂的机器，它的输入和输出之间存在错综复杂的耦合关系，那么 Schur 分解就是找到一组"自然坐标"，在这组坐标下，机器的作用变成了一个"级联结构"：第一级的输出影响第二级，第二级影响第三级，以此类推，但不存在反向的影响（上三角=无反馈）。而每一级的"增益"（对角元素）就是系统的特征值，它决定了系统在该模态下的放大或衰减行为。

酉变换的"旋转"性质则保证了这种坐标变换不会扭曲空间的度量——长度和角度在变换前后保持不变。这就好比在球面上重新选择经纬线：地球的形状没有改变，但在新的坐标系下，某些地理特征（如航线）可能变得更容易描述。

## 阅读建议与路线图

**入门阶段**：

- Sheldon Axler, *Linear Algebra Done Right*（第3版，Springer, 2015）——该书以"无行列式"的方式发展线性代数，Schur 定理是其第六章的核心内容，证明简洁而具有启发性。
- Gilbert Strang, *Introduction to Linear Algebra*（第6版，Wellesley-Cambridge Press, 2023）——从计算角度理解 Schur 分解与 QR 算法的联系。

**进阶阶段**：

- Roger Horn & Charles Johnson, *Matrix Analysis*（第2版，Cambridge University Press, 2013）——第2章系统讨论酉三角化及其推论，是矩阵分析领域的标准参考。
- Gene Golub & Charles Van Loan, *Matrix Computations*（第4版，Johns Hopkins University Press, 2013）——第7章详述 QR 算法的实现细节与 Schur 分解的数值计算。

**专题深入**：

- Nicholas Higham, *Functions of Matrices: Theory and Computation*（SIAM, 2008）——第1章与第9章展示 Schur 分解在矩阵函数计算中的核心作用。
- Lloyd N. Trefethen & David Bau III, *Numerical Linear Algebra*（SIAM, 1997）——从数值分析角度阐释 Schur 分解的稳定性与算法意义。

**原始文献**：

- Schur, I., "Über die charakteristischen Wurzeln einer linearen Substitution mit einer Anwendung auf die Theorie der Integralgleichungen," *Mathematische Annalen*, Vol. 66, pp. 488--510, 1909. 可通过 Springer 数字档案获取。

**建议阅读路径**：Axler（概念理解） $\to$ Horn & Johnson（理论深化） $\to$ Golub & Van Loan（算法实现） $\to$ Higham（高级应用）。

## 局限性与未解决问题

尽管 Schur 定理在理论与计算中具有核心地位，但它也存在若干固有局限：

**（一）非唯一性**：Schur 分解不具有唯一性——特征值在对角线上的排列顺序是任意的，且当特征值有重数时，酉因子 $Q$ 的选择自由度更大。这与 Jordan 标准形（在块排列顺序确定后唯一）形成对比。在需要唯一标准形的理论问题中，Schur 分解不如 Jordan 形式方便。

**（二）实数域的限制**：Schur 定理在复数域上成立（依赖代数基本定理）。对于实矩阵，只能得到"实 Schur 形式"——准上三角矩阵，其中复共轭特征值对对应 $2 \times 2$ 的实块。这增加了理论表述和算法实现的复杂性。

**（三）结构信息的损失**：与 Jordan 标准形相比，Schur 形式丢失了关于特征值代数重数与几何重数之差（即 Jordan 块结构）的精细信息。Schur 形式中严格上三角部分的元素虽然包含这些信息，但它们不是相似不变量，依赖于酉矩阵的选择。

**（四）无穷维推广的困难**：Schur 定理是有限维的结果。在无穷维 Hilbert 空间中，紧算子可以进行类似的三角化（Ringrose 定理，1962），但一般有界算子的三角化问题——不变子空间问题——至今仍是泛函分析中最著名的未解决问题之一。具体而言：是否每个可分 Hilbert 空间上的有界线性算子都具有非平凡的不变子空间？这一问题自20世纪30年代提出以来，虽然在特殊类别（紧算子、正规算子、多项式有界算子等）中已获解决，但一般情形仍然悬而未决。

**（五）结构化矩阵的 Schur 形式**：对于具有特殊结构的矩阵（如 Hamiltonian 矩阵、辛矩阵、正交辛矩阵），普通的 Schur 分解不保持这些结构。发展保结构的 Schur 分解（如 Hamiltonian Schur 形式）是数值线性代数中的活跃研究方向。

## 相关重要后续论文

1. **Francis, J. G. F.** (1961--1962). "The QR Transformation: A Unitary Analogue to the LR Transformation," *The Computer Journal*, 4(3):265--271 与 4(4):332--345. 确立了 Schur 分解的数值计算方法——QR 算法，被列为20世纪十大算法之一。

2. **Kublanovskaya, V. N.** (1961). "On some algorithms for the solution of the complete eigenvalue problem," *USSR Computational Mathematics and Mathematical Physics*, 1(3):637--657. 独立于 Francis 发明 QR 算法，从 LQ 分解的角度构造。

3. **Haynsworth, E. V.** (1968). "Determination of the inertia of a partitioned Hermitian matrix," *Linear Algebra and its Applications*, 1(1):73--81. 命名了 Schur 补并建立了惯性指数的加法公式。

4. **Golub, G. H. & Uhlig, F.** (2009). "The QR algorithm: 50 years later its genesis by John Francis and Vera Kublanovskaya and subsequent developments," *IMA Journal of Numerical Analysis*, 29(2):467--485. QR 算法发明五十周年的权威历史回顾。

5. **Ringrose, J. R.** (1962). "Super-diagonal forms for compact linear operators," *Proceedings of the London Mathematical Society*, 12(1):367--384. 将 Schur 三角化推广到可分 Hilbert 空间上的紧算子。

6. **Parlett, B. N.** (1976). "A recurrence among the elements of functions of triangular matrices," *Linear Algebra and its Applications*, 14(2):117--121. 建立了上三角矩阵函数值的递推计算公式，与 Schur 分解结合构成 Schur-Parlett 算法。

## 进一步阅读

- **原始论文**：Schur, I. (1909), [*Über die charakteristischen Wurzeln einer linearen Substitution mit einer Anwendung auf die Theorie der Integralgleichungen*](https://link.springer.com/article/10.1007/BF01450045), Math. Ann. 66, 488--510.
- **Schur 分析贡献综述**：Dym, H. (2007), [*Contributions of Issai Schur to Analysis*](https://arxiv.org/pdf/0706.1868), arXiv:0706.1868.
- **Schur 传记**：[MacTutor History of Mathematics: Issai Schur](https://mathshistory.st-andrews.ac.uk/Biographies/Schur/).
- **Schur 分解百科**：[Wikipedia: Schur Decomposition](https://en.wikipedia.org/wiki/Schur_decomposition).
- **Schur 补专著**：Zhang, F. (Ed.), *The Schur Complement and Its Applications*, Springer, 2005.
- **矩阵分析**：Horn, R. & Johnson, C., *Matrix Analysis*, 2nd ed., Cambridge University Press, 2013.
- **数值线性代数**：Golub, G. & Van Loan, C., *Matrix Computations*, 4th ed., Johns Hopkins University Press, 2013.
- **矩阵函数**：Higham, N., *Functions of Matrices: Theory and Computation*, SIAM, 2008.
- **QR 算法历史**：Golub, G. & Uhlig, F. (2009), [*The QR algorithm: 50 years later*](https://www.math.unipd.it/~alvise/AN_2016/LETTURE/QR_50_years_later.pdf), IMA J. Numer. Anal. 29(2), 467--485.
- **Hilbert 积分方程理论**：Hilbert, D., *Grundzüge einer allgemeinen Theorie der linearen Integralgleichungen*, Teubner, 1912.
