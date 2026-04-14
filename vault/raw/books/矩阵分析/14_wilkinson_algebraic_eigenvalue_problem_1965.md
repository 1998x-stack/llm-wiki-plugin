# Wilkinson《代数特征值问题》（1965）：数值线性代数的奠基之作

## 作者

**James Hardy Wilkinson**（詹姆斯·哈迪·威尔金森，1919年9月27日--1986年10月5日），英国数学家，现代数值线性代数的奠基人。1970年ACM图灵奖得主，1969年当选英国皇家学会院士（FRS），是现代数值分析领域首位获此殊荣的学者。Wilkinson早年就读于剑桥大学三一学院，师从G. H. Hardy、J. E. Littlewood和A. S. Besicovitch等数学巨匠，以一等荣誉学位毕业。二战期间从事弹道计算工作，1946年加入英国国家物理实验室（NPL），在那里与Alan Turing共同参与了ACE（Automatic Computing Engine）计算机的设计工作，并亲手设计了Pilot ACE的乘法运算单元。这段与早期电子计算机朝夕相处的经历，使他深刻体会到浮点运算舍入误差对计算结果的深远影响，从而开创了后向误差分析（backward error analysis）这一革命性方法论。

## 发表时间与出版信息

本书于**1965年**由牛津大学出版社旗下的Clarendon Press出版，全书共662页，初版定价110先令。该书被纳入"Monographs on Numerical Analysis"丛书系列，后于1988年以"Numerical Mathematics and Scientific Computation"系列再版（ISBN: 978-0-19-853418-1）。作为数值分析领域引用率最高的专著之一，该书自出版以来从未绝版，至今仍被全球各大学图书馆列为数值线性代数课程的核心参考文献。

## 一句话概括

本书系统建立了矩阵特征值与特征向量计算的误差分析理论框架，以后向误差分析为核心方法论，奠定了现代数值线性代数的理论基础与算法分析范式。

## 历史背景

20世纪40年代末至60年代中期，人类正经历一场深刻的计算革命。1946年ENIAC的诞生标志着电子计算机时代的到来，此后短短二十年间，从EDVAC、UNIVAC到IBM 704、7090，计算机的运算速度提升了数个数量级。然而，计算能力的飞跃也带来了一个根本性的理论挑战：当数以千计的浮点运算在机器内部以有限精度执行时，每一步都会引入微小的舍入误差（rounding error），这些误差的累积效应是否会使最终结果变得毫无意义？

这一忧虑并非杞人忧天。1943年，统计学家Harold Hotelling发表了一篇影响深远的论文，声称Gauss消去法在求解线性方程组时，舍入误差会随方程维数呈指数级增长——这一结论若为真，将意味着大规模矩阵计算在原理上就不可靠。Hotelling的悲观预言在科学界引发了广泛的焦虑。1947年，John von Neumann与Herman Goldstine在美国数学学会通报上发表了里程碑式论文"Numerical Inverting of Matrices of High Order"，首次系统地区分了数学问题本身的"病态性"（ill-conditioning）与数值算法的"不稳定性"（instability），引入了条件数的原型概念，被Wilkinson本人赞誉为"奠定了现代误差分析的基础"。然而，von Neumann和Goldstine的分析局限于正定矩阵，无法处理一般情形。1948年，Alan Turing在论文"Rounding-off Errors in Matrix Processes"中将分析推广到一般矩阵，引入了"条件数"（condition number）这一术语——面对von Neumann都未能解决的问题，Turing展现了惊人的勇气与雄心。

但即便有了这些先驱性工作，到1960年代初，数值分析仍然缺乏一套统一、严格且实用的误差分析方法论。现有的"正向误差分析"（forward error analysis）试图直接追踪每一步运算中误差的传播，这在理论上简洁，但在实际算法（往往包含数百万步运算）中几乎不可操作——误差界要么过于悲观（远超实际误差），要么无法给出（分析过于复杂）。与此同时，特征值问题作为科学计算中最核心的计算任务之一——从量子力学中的能级计算到结构工程中的振动分析——亟需可靠的算法与严格的理论保证。正是在这一历史背景下，Wilkinson凭借其在NPL与Pilot ACE计算机十余年的实际计算经验，以及深厚的数学功底，完成了这部划时代的著作。

## 核心问题

本书致力于回答一个根本性的问题：**对于求解矩阵特征值和特征向量的各类数值算法，我们如何严格地分析其数值稳定性，并精确地评估计算结果的可靠程度？**

特征值问题（eigenvalue problem）是线性代数中最基本也最重要的问题之一：给定 $n \times n$ 矩阵 $A$，求标量 $\lambda$ 和非零向量 $x$ 使得 $Ax = \lambda x$。这一数学结构广泛出现在量子力学（Hamilton算子的本征值即能级）、结构工程（振动频率分析）、控制理论（系统稳定性判据）和统计学（主成分分析）等领域。在计算机上求解这一问题时，必须面对浮点运算固有的舍入误差，而特征值对矩阵元素的微小变化可能极其敏感——著名的"Wilkinson多项式"就是一个令人震惊的例子：一个20次多项式的某个系数仅改变 $2^{-23}$，就会导致某些根发生数量级的偏移。

具体而言，本书的核心问题可以分解为以下子问题：（1）当算法在有限精度浮点算术下执行时，舍入误差对计算得到的特征值和特征向量的影响有多大？（2）这种影响在多大程度上取决于算法的选择，又在多大程度上取决于问题本身的内在敏感性？（3）能否建立一套统一的理论框架，使我们对不同算法的数值行为做出定量的、可比较的评估？（4）如何设计出在数值稳定性意义下最优的算法？

## 主要定理与结果

### 后向误差分析框架

本书最核心的理论贡献是系统建立了**后向误差分析**（backward error analysis）的方法论框架。其基本思想可以用一个优雅的命题表述：

**定理（后向误差分析原理）**：设算法A在浮点算术下对输入矩阵 $A$ 计算得到的结果为 $\hat{x}$，则存在一个扰动矩阵 $\delta A$，使得 $\hat{x}$ 恰好是扰动问题 $(A + \delta A)$ 的精确解，且

$$\frac{\|\delta A\|}{\|A\|} \leq f(n) \cdot \varepsilon_{\text{mach}}$$

其中 $n$ 为矩阵维数，$\varepsilon_{\text{mach}}$ 为机器精度（machine epsilon），$f(n)$ 是一个温和增长（通常为低阶多项式）的函数。

这一框架将"计算结果有多好"的问题转化为"计算结果精确地解了哪个问题"，其深刻之处在于：一旦后向误差 $\|\delta A\|/\|A\|$ 足够小（与输入数据本身的不确定性可比拟），则算法就是"后向稳定的"（backward stable），计算结果的精度完全由问题本身的条件数决定，而非算法的具体实现。

### 条件数理论

Wilkinson在书中系统发展了特征值问题的条件数理论。对于一般矩阵 $A = V \Lambda V^{-1}$（其中 $V$ 为特征向量矩阵，$\Lambda$ 为特征值对角矩阵），特征值的条件数为：

$$\kappa(\lambda_i) = \frac{1}{|y_i^H x_i|}$$

其中 $x_i$ 和 $y_i$ 分别为对应于特征值 $\lambda_i$ 的右特征向量和左特征向量。这个结果表明，当左右特征向量接近正交时（即 $|y_i^H x_i| \to 0$），特征值对扰动极为敏感。对于Hermite矩阵，所有特征值的条件数均为1——这从理论上解释了为何对称特征值问题在数值上远比一般问题"容易"。

与此相关的是1960年Bauer和Fike建立的经典扰动界：设 $\mu$ 为 $(A + \delta A)$ 的任意特征值，则存在 $A$ 的特征值 $\lambda$ 使得

$$|\lambda - \mu| \leq \kappa_p(V) \cdot \|\delta A\|_p$$

其中 $\kappa_p(V) = \|V\|_p \cdot \|V^{-1}\|_p$ 为特征向量矩阵的条件数。Wilkinson在书中系统整合并深化了这些扰动界的理论意义与实际应用。

### QR算法的收敛性分析与Wilkinson位移

本书对QR算法进行了迄今最为深入的收敛性分析。QR算法由John G. F. Francis（1961年，英国）和Vera N. Kublanovskaya（1961年，苏联）独立发现，是计算矩阵特征值最重要的算法之一。Wilkinson在书中证明了：

**带位移QR算法的收敛性**：对于对称三对角矩阵，采用Wilkinson位移（即选择2x2尾部子矩阵的特征值中更接近末元素的那个作为位移量 $\mu_k$）的QR迭代具有**全局收敛性**，且渐近收敛速度至少为**三次方**（cubic convergence）。

$$\mu_k = a_{nn} - \frac{\text{sign}(\delta) \cdot b_{n-1}^2}{|\delta| + \sqrt{\delta^2 + b_{n-1}^2}}, \quad \delta = \frac{a_{n-1,n-1} - a_{nn}}{2}$$

这一位移策略（后被称为"Wilkinson位移"）在实际计算中表现卓越：对于典型的对称特征值问题，每个特征值的隔离（deflation）通常只需一到两次迭代，使得整个算法的计算复杂度约为 $O(n^3)$。

### Gauss消去法的后向稳定性

Wilkinson还给出了带部分主元选取（partial pivoting）的Gauss消去法的经典后向误差界：

$$\|A + \delta A\| \leq 8n^3 \rho_n \varepsilon_{\text{mach}} \|A\|$$

其中 $\rho_n$ 为增长因子（growth factor）。他通过大量实际计算经验和理论分析表明，尽管 $\rho_n$ 在最坏情况下可以达到 $2^{n-1}$，但在实际问题中几乎总是保持为适度大小——这一结论彻底推翻了Hotelling关于Gauss消去法不可靠的悲观判断。

## 核心方法

Wilkinson在本书中运用并发展了以下核心方法论：

**后向误差分析**是全书的灵魂。与传统的正向误差分析（试图直接估计 $\|\hat{x} - x\|$）不同，后向分析将浮点运算产生的所有舍入误差"吸收"到输入数据的扰动中，从而将一个几乎不可能追踪的误差累积问题，转化为一个干净的扰动分析问题。Wilkinson自述这一方法最初源于他在Pilot ACE上计算多项式零点的经验——当他发现计算出的零点虽然不是原多项式的精确零点，但却是一个系数微小扰动后的多项式的精确零点时，后向误差分析的思想由此萌生。

**矩阵范数与扰动理论**的系统应用是第二个方法论支柱。Wilkinson熟练运用算子范数、Frobenius范数等工具，将离散的逐元素误差估计提升为优雅的矩阵级别不等式，使得误差分析具有了内在的几何直觉。

**正交变换的数值优越性**是贯穿全书的第三个主题。Wilkinson系统论证了Givens旋转（由Wallace Givens于1958年提出）和Householder反射（由Alston Householder于1958年提出）等正交变换在数值计算中的内在稳定性——因为正交变换保持向量的2-范数不变，故不会放大误差。这一洞察直接指导了后续所有数值线性代数算法的设计哲学。

## 重要性与影响

《代数特征值问题》的出版，标志着数值线性代数从一门经验性的技艺转变为一门有严格理论基础的科学。在此之前，人们对数值算法的评估主要依靠直觉和实验；在此之后，每一个新算法都必须附带严格的后向误差分析——否则就不会被学术界和工程界接受。正如一位同行所言："在我看来，Wilkinson几乎以一己之力创造了我们目前关于线性代数计算机解法的全部科学知识。"

这部著作彻底改变了数值分析的思维范式。在Wilkinson之前，数值分析家问的是"计算结果离真实值有多远"（正向误差）；在Wilkinson之后，人们学会了问"计算结果精确地解了哪个问题"（后向误差）。这一思维方式的转换看似简单，却具有革命性的意义：它将算法稳定性与问题条件性清晰地分离开来，使得"好算法"有了客观的判定标准——后向稳定的算法就是好算法，而计算结果的精度则完全由问题的条件数来决定。

该书奠定了计算数学软件工程的方法论基础。1970年代，Jack Dongarra等人在开发LINPACK（线性方程组求解）和EISPACK（特征值计算）软件包时，直接以Wilkinson的误差分析理论作为算法选择与质量评估的标准。LAPACK用户指南的扉页上写道："本工作献给Jim Wilkinson，他的思想与精神在项目的每一个环节都给予我们启迪和影响。"从EISPACK到LINPACK，再到今天的LAPACK、ScaLAPACK、MATLAB、NumPy/SciPy——这条贯穿半个世纪的数值计算软件发展链条，其理论根基正是Wilkinson在本书中建立的。

## 解决了什么瓶颈

在本书出版之前，数值计算面临一个根本性的信任危机：科学家和工程师无法确信计算机给出的结果到底有多可靠。Hotelling关于误差指数增长的悲观预言更是雪上加霜。Von Neumann和Turing虽然各自贡献了重要的理论洞见，但他们的分析要么局限于特殊情形（正定矩阵），要么未能形成系统的方法论。

Wilkinson的后向误差分析框架一举解决了这一瓶颈。通过将"计算误差有多大"转化为"输入扰动有多大"，他为科学计算提供了一个既严格又实用的可靠性保证：只要后向误差与输入数据的测量不确定性在同一量级，计算结果就是"可以信赖的"。这一理论框架也为算法设计提供了明确的目标——设计后向稳定的算法——从而结束了此前算法评估中的主观臆断和无所适从。

## 与前人工作的关系

本书的理论体系建立在三大先驱性工作之上。**Von Neumann与Goldstine（1947）**的论文首次将严格的数学分析引入数值计算领域，建立了条件数概念的原型，区分了问题的病态性与算法的不稳定性。**Turing（1948）**将条件数理论推广到一般矩阵，并为Gauss消去法提供了更广泛适用的误差分析。**Givens（1958）和Householder（1958）**分别发展了正交旋转和正交反射方法，为数值稳定的矩阵分解提供了基本构件。

Wilkinson对这些工作既有继承又有超越。他继承了von Neumann和Turing关于"区分问题与算法"的基本思想，但将其发展为一套完整的、可操作的方法论——后向误差分析。他继承了Givens和Householder关于正交变换优越性的认识，但将其整合到一个统一的理论框架中，并通过严格的误差分析证明了这种优越性的数学本质。尤其值得注意的是，尽管Turing和von Neumann都在思考相关问题，但后向误差分析这一关键思想并未出现在他们任何一人的工作中——这或许是因为，只有Wilkinson这样在实际计算机上进行过大量矩阵运算的数学家，才能从计算实践中提炼出如此深刻的理论洞见。

Wilkinson自己在1970年的图灵奖演讲中回忆道，后向误差分析的思想最初来自他在Pilot ACE上计算多项式零点的经验，随后在特征值计算中得到系统发展。他曾在二战期间用手摇计算器解12阶线性方程组的经历，也为他日后理解舍入误差提供了无可替代的直觉。

## 对后续工作的影响

本书的影响广泛而深远，几乎涵盖了数值线性代数的每一个分支。

**软件工程层面**：Wilkinson与C. Reinsch合编的《Handbook for Automatic Computation, Vol. 2: Linear Algebra》（1971）直接脱胎于本书的理论框架，其中超过一半的算法贡献来自Wilkinson本人。该手册中的Algol程序后来被翻译为Fortran，成为EISPACK和LINPACK的核心，进而演化为今天广泛使用的LAPACK——这是科学计算领域最重要的基础设施之一。

**教材与教育层面**：Gene H. Golub与Charles F. Van Loan的经典教材《Matrix Computations》（1983年初版，2013年第四版）在很大程度上是对Wilkinson工作的现代化阐释和扩展。作者在序言中将Wilkinson（1965）列为全书的"全局参考文献"之首。G. W. Stewart的《Introduction to Matrix Computations》（1973）和Beresford Parlett的《The Symmetric Eigenvalue Problem》（1980）同样深受Wilkinson的影响。

**理论研究层面**：G. W. Stewart和Ji-guang Sun的《Matrix Perturbation Theory》（1990）将Wilkinson开创的扰动分析推向了更高的系统性和一般性。Nicholas Higham的《Accuracy and Stability of Numerical Algorithms》（1996，2002年第二版）则是后向误差分析方法论在更广泛数值算法领域的集大成之作。

**荣誉与纪念**：SIAM于1982年设立了"J. H. Wilkinson数值分析与科学计算奖"，1991年又设立了"J. H. Wilkinson数值软件奖"，两个奖项至今仍是数值计算领域的最高荣誉之一。

## 现代价值

尽管距初版已逾六十年，本书建立的理论框架在当代计算科学中依然具有核心价值。

**机器学习与深度学习**：神经网络训练本质上是大规模矩阵运算的迭代过程。随着混合精度训练（mixed-precision training）和低精度推理（如FP16、BF16、INT8）的普及，Wilkinson的后向误差分析理论为理解低精度运算下模型训练的数值稳定性提供了不可或缺的理论工具。特征值分解在主成分分析（PCA）、谱聚类、推荐系统等核心算法中无处不在。

**大规模科学计算**：从量子化学中的电子结构计算到结构工程中的有限元分析，大规模稀疏矩阵的特征值计算仍然是科学计算的核心任务。现代迭代方法（如Lanczos算法、Arnoldi方法）的数值稳定性分析，本质上仍在Wilkinson建立的理论框架内进行。

**量子计算**：量子计算模拟器需要处理指数级维度的酉矩阵和Hermite矩阵的特征值问题。量子纠错码的设计和量子算法的经典验证，都离不开对矩阵特征值计算精度的严格保证。

**数据科学与信号处理**：奇异值分解（SVD）——与特征值分解密切相关——是数据降维、推荐系统、自然语言处理中词嵌入等技术的数学基础。Wilkinson的条件数理论帮助工程师判断何时计算结果可以信赖，何时问题本身的病态性已使结果不可靠。

**高性能计算与硬件协同设计**：随着专用加速硬件（TPU、NPU等）的兴起，低精度浮点格式（如Google的bfloat16、Nvidia的TF32）被广泛用于加速矩阵运算。在这些非标准精度下，Wilkinson建立的后向误差分析框架成为评估计算结果可靠性的唯一理论依据。混合精度算法（先用低精度快速计算，再用高精度迭代精化）的正确性证明，本质上就是多层嵌套的后向误差分析。可以说，在计算精度日益多样化的当代，Wilkinson的理论不是越来越过时，而是越来越不可或缺。

## 通俗解读

后向误差分析的精髓可以用一个日常比喻来理解。

设想你用一把精度有限的尺子（比如最小刻度1毫米）去测量一张桌子的长度。你的测量结果是1523毫米，而桌子的真实长度可能是1523.4毫米——你有约0.4毫米的测量误差。现在假设有人用精密仪器测出另一张桌子的长度恰好是1523.000毫米，那么你的测量结果对这张桌子来说就是完美精确的。

后向误差分析的哲学完全类似。当计算机用有限精度浮点运算来求解一个矩阵问题时，计算结果不会是原始问题的精确解，但它是某个"稍微不同的问题"的精确解。后向误差分析要问的是：这个"稍微不同的问题"与原问题到底差多少？如果差异小于输入数据本身的测量误差或不确定性——正如你的尺子本来就只有1毫米的精度——那么计算结果就已经是"在实际意义上完美的"。

这种思维方式的革命性在于：它把"算法好不好"和"问题难不难"清晰地分开了。一个后向稳定的算法就像一个合格的测量员——他忠实地用手中的工具做到了最好；而结果的最终精度取决于测量工具本身（机器精度）和被测对象的特性（条件数）。如果一个形状极其不规则的物体即使用精密仪器也难以准确测量，那不是测量员的错——这就是"病态问题"的本质。

## 阅读指南

对于不同背景的读者，建议采用以下阅读路径：

**入门读者**（本科高年级/研究生初学者）：建议先阅读第一章"理论背景"（Theoretical Background）和第二章"扰动理论"（Perturbation Theory），建立矩阵特征值问题的基本概念和扰动敏感性的直觉。然后跳至第五章"Hermite矩阵"（Hermitian Matrices），因为对称/Hermite情形理论最为完整，也最容易理解。

**算法研究者**：在掌握前两章基础后，重点研读第三章"误差分析"（Error Analysis）——这是后向误差分析方法论的核心展示。随后第八章"LR与QR算法"是算法收敛性分析的精华。

**软件开发者**：建议特别关注第四章"线性代数方程的解法"和第六章"一般矩阵化为紧凑形"，这两章的内容直接对应LAPACK中的核心子程序。

**历史兴趣者**：第九章"迭代方法"（Iterative Methods）讨论了幂法（power method）、反迭代法（inverse iteration）等经典迭代技术，虽然这些方法在现代大规模计算中已被更先进的Krylov子空间方法所取代，但它们的理论分析仍然是理解现代方法的基础。此外，书中各章节中穿插的历史注记和对前人工作的评述，生动地勾勒了数值线性代数这一学科从萌芽到成熟的发展历程，具有独特的史料价值。

**补充阅读**：由于本书写于1965年，一些后续发展（如分治法、多重网格法、随机化算法）未被涵盖。建议配合Golub与Van Loan的《Matrix Computations》第四版（2013）和Higham的《Accuracy and Stability of Numerical Algorithms》第二版（2002）进行补充学习。对于稀疏矩阵特征值计算，可参阅Yousef Saad的《Numerical Methods for Large Eigenvalue Problems》（2011年修订版）。

## 局限性

客观地说，本书也有其历史局限性。

**稀疏矩阵方法的缺席**：全书的分析框架主要针对稠密矩阵（dense matrix）。对于大规模稀疏矩阵的特征值计算——如Lanczos算法和Arnoldi方法——书中未做系统讨论。这些迭代方法在1960年代尚处于早期发展阶段，其理论分析要到Paige（1971年关于Lanczos算法数值稳定性的博士论文）和后续工作中才逐步成熟。

**并行计算视角的缺乏**：本书写于串行计算机时代，完全未涉及算法的并行化问题。随着多核处理器和GPU计算的兴起，算法的并行效率已成为与数值稳定性同等重要的设计考量。

**非对称特征值问题的部分遗憾**：尽管书中对一般矩阵（非对称/非Hermite）有所讨论，但理论的完整性和优美性不及对称情形。非正规矩阵（non-normal matrix）的伪谱（pseudospectrum）理论——由Lloyd N. Trefethen在1990年代系统发展——提供了超越经典条件数的更细致刻画，这一方向自然超出了本书的时代范围。

**数值实验的时代印记**：书中的数值示例都是在1960年代的计算机上完成的，机器精度、问题规模和计算速度与今天不可同日而语。虽然理论结论不受影响，但读者需要将书中的数值经验映射到当代计算环境中去理解。

## 延伸阅读

1. **Wilkinson, J. H.** *Rounding Errors in Algebraic Processes*. Englewood Cliffs, NJ: Prentice-Hall, 1963. -- Wilkinson的第一本书，比本书更简洁，专注于舍入误差分析的基本原理，是理解本书方法论的极佳预备读物。

2. **Golub, G. H. & Van Loan, C. F.** *Matrix Computations*. 4th ed. Baltimore: Johns Hopkins University Press, 2013. -- 数值线性代数领域最广泛使用的教材，被誉为Wilkinson著作的现代继承者，覆盖了本书出版后半个世纪的算法发展。

3. **Higham, N. J.** *Accuracy and Stability of Numerical Algorithms*. 2nd ed. Philadelphia: SIAM, 2002. -- 将Wilkinson的后向误差分析方法论推广到更广泛的数值算法领域，堪称本书方法论精神的集大成者。

4. **Parlett, B. N.** *The Symmetric Eigenvalue Problem*. Englewood Cliffs, NJ: Prentice-Hall, 1980; reprinted SIAM, 1998. -- 对称特征值问题的权威专著，深化并扩展了Wilkinson在这一专题上的工作。

5. **Stewart, G. W. & Sun, J.-g.** *Matrix Perturbation Theory*. Boston: Academic Press, 1990. -- 系统发展了Wilkinson开创的矩阵扰动理论，涵盖特征值、特征子空间和不变子空间的扰动分析。

6. **Trefethen, L. N. & Bau, D.** *Numerical Linear Algebra*. Philadelphia: SIAM, 1997. -- 面向研究生的现代数值线性代数教材，以清新的风格重新阐释了包括后向误差分析在内的核心理论。

7. **Wilkinson, J. H. & Reinsch, C. (eds.)** *Handbook for Automatic Computation, Vol. II: Linear Algebra*. New York: Springer-Verlag, 1971. -- 将本书的理论成果转化为经过严格测试的算法实现，是EISPACK和LINPACK的直接前身。

8. **Saad, Y.** *Numerical Methods for Large Eigenvalue Problems*. Revised ed. Philadelphia: SIAM, 2011. -- 大规模稀疏矩阵特征值计算的权威参考，覆盖了Lanczos、Arnoldi等Krylov子空间方法，是本书在稀疏矩阵方向的重要补充。

## 参考文献

- Wilkinson, J. H. *The Algebraic Eigenvalue Problem*. Oxford: Clarendon Press, 1965. 662 pp.
- Wilkinson, J. H. *Rounding Errors in Algebraic Processes*. Englewood Cliffs, NJ: Prentice-Hall, 1963.
- von Neumann, J. & Goldstine, H. H. "Numerical Inverting of Matrices of High Order." *Bulletin of the American Mathematical Society*, 53(11): 1021--1099, 1947.
- Turing, A. M. "Rounding-off Errors in Matrix Processes." *Quarterly Journal of Mechanics and Applied Mathematics*, 1(1): 287--308, 1948.
- Bauer, F. L. & Fike, C. T. "Norms and Exclusion Theorems." *Numerische Mathematik*, 2(1): 137--141, 1960.
- Givens, W. "Computation of Plane Unitary Rotations Transforming a General Matrix to Triangular Form." *Journal of the Society for Industrial and Applied Mathematics*, 6(1): 26--50, 1958.
- Householder, A. S. "Unitary Triangularization of a Nonsymmetric Matrix." *Journal of the ACM*, 5(4): 339--342, 1958.
- Francis, J. G. F. "The QR Transformation: A Unitary Analogue to the LR Transformation." *The Computer Journal*, 4(3): 265--271, 1961.
- Golub, G. H. & Van Loan, C. F. *Matrix Computations*. 4th ed. Baltimore: Johns Hopkins University Press, 2013.
- Higham, N. J. *Accuracy and Stability of Numerical Algorithms*. 2nd ed. Philadelphia: SIAM, 2002.
- Parlett, B. N. *The Symmetric Eigenvalue Problem*. Englewood Cliffs, NJ: Prentice-Hall, 1980.
- Stewart, G. W. & Sun, J.-g. *Matrix Perturbation Theory*. Boston: Academic Press, 1990.
- Wilkinson, J. H. & Reinsch, C. (eds.) *Handbook for Automatic Computation, Vol. II: Linear Algebra*. New York: Springer-Verlag, 1971.
- ACM Turing Award Citation for J. H. Wilkinson, 1970. Association for Computing Machinery.
