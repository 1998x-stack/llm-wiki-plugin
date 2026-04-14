# Golub--Van Loan《矩阵计算》（1983）：计算线性代数的百科全书

## 作者

**Gene H. Golub**（吉恩·戈卢布，1932--2007）与 **Charles F. Van Loan**（查尔斯·范·洛恩，1946--）

Gene H. Golub 于1932年2月29日出生在芝加哥一个拉脱维亚-乌克兰移民家庭，先后在 Wright Junior College 和 University of Illinois at Urbana-Champaign 就读，于1959年获得数学博士学位。1962年他加入 Stanford 大学计算机科学系，成为该系的创始成员之一，并于1981至1985年担任系主任。Golub 一生发表约250篇论文、合著18部著作，当选美国国家科学院院士和美国国家工程院院士，曾任 SIAM（Society for Industrial and Applied Mathematics）主席，创办了 SIAM Journal on Scientific Computing 和 SIAM Journal on Matrix Analysis and Applications 两大期刊，被誉为"数值分析的教父"。他于2007年11月16日因急性髓系白血病去世。

Charles F. Van Loan 出生于新泽西州，在 University of Michigan 先后获得学士（1969）、硕士（1970）和博士（1973）学位，师从 Cleve Moler。在 University of Manchester 完成博士后研究后，他于1975年加入 Cornell 大学计算机科学系，1987年升任正教授，1998年获 Joseph C. Ford 工程讲席教授称号，1999至2006年担任系主任。2016年退休后出任 Cornell 大学教务长。2018年，Van Loan 获得 SIAM 最高荣誉之一的 John von Neumann Lecture Prize，以表彰他对数值线性代数研究与教学的卓越贡献。

---

## 发表时间与出版信息

- **第1版**：1983年，Johns Hopkins University Press 出版，476页
- **第2版**：1989年，扩充至642页，增加了大量迭代方法内容
- **第3版**：1996年，694页，全面修订，加入并行计算初步讨论
- **第4版**：2013年，756页，全面扩充约25%，新增张量计算、矩阵函数、大规模稀疏SVD、多重网格、Jacobi-Davidson 方法等章节

该书被纳入 Johns Hopkins Studies in the Mathematical Sciences 丛书，是该出版社迄今被引用最多的学术著作之一。全书致献给数值线性代数的两位奠基人 Alston S. Householder 和 James H. Wilkinson。

---

## 一句话概括

本书系统整理了矩阵计算的全部核心算法，以矩阵分解为组织原则，将理论分析、算法设计与误差控制融为一体，成为数值线性代数领域最具影响力的参考书和事实上的学科标准。

---

## 历史背景

从1940年代电子计算机诞生起，线性代数计算就是科学计算的核心任务。然而，在1960至1980年代之间，数值线性代数经历了一场从"分散知识"到"系统学科"的深刻转变，《矩阵计算》正是这一转变的集大成之作。

这一历史进程始于 James H. Wilkinson 在英国国家物理实验室（NPL）的开创性工作。Wilkinson 的1965年巨著 *The Algebraic Eigenvalue Problem* 第一次对特征值问题进行了系统的舍入误差分析，确立了"向后误差分析"（backward error analysis）这一核心方法论。Wilkinson 证明了一个深刻的洞见：数值算法的稳定性不在于它能否给出精确解，而在于它给出的近似解是否恰好是某个"微扰问题"的精确解。这一思想深刻影响了整个数值分析领域。1971年，Wilkinson 和 Reinsch 编辑出版了 *Handbook for Automatic Computation, Volume II: Linear Algebra*，收录了一系列高质量的 Algol 60 程序，成为后续软件开发的蓝本。

与此同时，美国的软件工程实践也在快速推进。1970年代，Argonne 国家实验室主导开发了 EISPACK（特征值计算软件包，1972--1978）和 LINPACK（线性方程组求解软件包，1977--1979），它们将 Wilkinson-Reinsch Handbook 中的算法翻译为 Fortran 并进行了工程化封装。LINPACK 由 Jack Dongarra、Jim Bunch、Cleve Moler 和 G. W. Stewart 共同开发，首创了通过调用 BLAS（Basic Linear Algebra Subprograms）实现可移植高性能的设计范式。值得注意的是，Cleve Moler 在1970年代末基于 LINPACK 和 EISPACK 创建了最初版本的 MATLAB，作为一个简单的交互式矩阵计算器。

在学术层面，George Forsythe 于1960年代在 Stanford 建立了计算数学研究方向，吸引了 Cleve Moler、Beresford Parlett、James Varah 等一批杰出学生。当 Forsythe 转向行政工作后，Golub 接过了数值分析方向的学术领导权。Golub 在 Stanford 建立起一个活跃的研究群体，与世界各地的访问学者保持密切合作。他最重要的技术贡献之一是1965年与 William Kahan 合作提出的 SVD 计算算法。在此之前，SVD 主要被视为一个理论概念；Golub-Kahan 算法使其成为可实际计算的工具。1970年 Golub 和 Christian Reinsch 发表了该算法的改进版本，被收录进 Wilkinson-Reinsch Handbook，并沿用至今。

G. W. Stewart 在1973年出版了 *Introduction to Matrix Computations*，是当时为数不多的系统性教科书。但到1980年代初，数值线性代数的知识仍然分散在数百篇论文、技术报告和几本各有侧重的专著中。学生和工程师要全面掌握该领域，需要阅读大量原始文献。正是在这样的背景下，Golub 和他在 Cornell 的年轻合作者 Van Loan 着手编写一部"一站式参考书"。Nick Higham 回忆说，他作为硕士生在1983年春天拿到本书第一版时的感受是"一种启示"（a revelation）——这本书提供了"对该学科全新的、最新的视角"。

---

## 核心问题

如何为矩阵计算中的所有核心问题——线性方程组求解、最小二乘问题、特征值问题、奇异值分解——给出统一的算法描述框架，并为每种算法提供严格的舍入误差分析和实际性能评估？换言之，如何将一个横跨代数、分析和计算机科学三个领域的庞大知识体系组织成一部条理清晰、兼具理论深度和实用价值的参考著作？

这个问题的挑战在于：矩阵计算不是一个单一的技术领域，而是一个由多条相互交织的线索组成的复杂网络。线性方程组求解需要矩阵分解理论；特征值计算依赖正交变换技术；最小二乘问题连接着矩阵分解与统计回归；而奇异值分解则是理解矩阵几何结构的终极工具。在此之前，没有任何一本著作能够以统一的视角将这些主题串联起来，同时兼顾算法效率、数值稳定性和实际可编程性三个维度。Golub 和 Van Loan 找到了一个优雅的解决方案：以矩阵分解为纲，以误差分析为魂，以伪代码为载体，将整个知识体系有机地组织在一起。

---

## 主要定理与核心结果

《矩阵计算》并非以定理-证明的形式组织，而是以"矩阵分解"为核心线索，系统地展开以下关键结果：

**1. 矩阵分解理论体系**。全书围绕六大分解构建：LU 分解（Gaussian 消去法的矩阵语言）、Cholesky 分解（对称正定矩阵）、QR 分解（正交三角化）、奇异值分解（SVD）、Schur 分解（一般特征值问题）和广义特征值分解。每种分解都配套存在性定理、唯一性条件、算法实现和误差界。

**2. Householder 变换与 Givens 旋转**。书中详细阐述了这两种正交变换的构造和应用。Householder 变换将向量反射到坐标轴方向，是 QR 分解和二对角化的基本工具；Givens 旋转则逐元素地将矩阵化为三角或带状形式，适合处理结构化和稀疏矩阵。两者的数值稳定性分析是全书的亮点之一。

**3. SVD 的计算**。从 Golub-Kahan 二对角化算法到隐式 QR 迭代，本书给出了 SVD 计算的完整流程。SVD 将矩阵分解为 $A = U\Sigma V^T$，揭示了矩阵的几何本质：它将单位超球映射为超椭球，奇异值即为椭球的半轴长。

**4. 对称特征值问题**。包括 Jacobi 方法、三对角化后的 QR 迭代、分治法（divide-and-conquer）和二分法。书中证明了对称特征值问题具有优越的数值性质：特征值对扰动的敏感度仅与扰动大小成正比。

**5. 非对称特征值问题**。包括 Hessenberg 化简、QR 算法（Francis 双步隐式移位）和 Schur 分解。书中详细讨论了非对称问题的困难之处：特征值可能对扰动高度敏感（"病态特征值"），需要引入特征值条件数来量化。

**6. 迭代方法**。包括 Lanczos 迭代（对称大规模特征值问题）、Arnoldi 迭代（非对称情形）和共轭梯度法（大规模线性方程组）。第4版进一步扩展到 Jacobi-Davidson 方法和多重网格预处理。

**7. 扰动理论与误差分析**。全书贯穿 Wilkinson 式的向后误差分析传统。对每种算法，书中都给出了严格的舍入误差界，使读者能够预判算法在有限精度算术下的表现。

---

## 核心方法

本书最具创新性的方法论贡献是确立了"矩阵分解"作为整个数值线性代数的组织原则。这一视角的深刻之处在于：几乎所有矩阵计算问题都可以归结为"先做分解，再利用分解求解"的两步范式。

具体而言，本书的方法论框架包含三个层次：

**算法层**：每种分解对应一组高效算法，用 MATLAB 风格的伪代码精确描述。这种伪代码的特点是使用冒号记号表示子矩阵（如 $A(1\text{:}k, k\text{:}n)$），既简洁又与实际编程直接对应。第1版率先采用这种风格，后来成为数值分析教科书的标准写法。

**分析层**：每种算法配有严格的舍入误差分析和条件数讨论。书中系统地运用了矩阵范数、向后误差和条件数三个概念来刻画算法的数值行为。特别是对 Gaussian 消去法的增长因子分析、QR 分解的正交性损失分析等，堪称向后误差分析的典范。

**应用层**：每种分解都与具体的计算问题相联系，如 QR 分解用于最小二乘，SVD 用于低秩近似和伪逆计算，LU 分解用于一般线性方程组求解。这种"分解-算法-应用"的三位一体结构使本书既是理论参考，也是工程手册。

此外，书中对算法复杂度的讨论非常精细，用 flop（浮点运算次数）来精确计量不同算法的代价，使读者能够在实际应用中做出合理的算法选择。

---

## 重要性与影响

《矩阵计算》的影响力难以用简单的数字衡量，但一些指标仍然令人印象深刻。据 Google Scholar 统计，仅 Van Loan 一人的总引用量就超过118000次，而该书各版本的合计引用远超80000次，使其成为数学科学领域被引用最多的专著之一。该书不仅被全球数百所大学用作研究生教材或参考书，更重要的是，它定义了一个学科的话语体系和研究范式。

在教育层面，本书几乎以一己之力确立了"数值线性代数"作为独立课程的教学大纲。此前，矩阵计算的内容通常零散地分布在"数值分析"或"科学计算"课程中；《矩阵计算》证明了这个领域有足够的深度和广度支撑一门独立课程。此后出版的教材——如 Trefethen 和 Bau 1997年广受欢迎的 *Numerical Linear Algebra* ——都在某种程度上以《矩阵计算》为参照系。Trefethen-Bau 采用了更精巧的教学设计（40个讲座式短章节，以 QR 分解而非 Gaussian 消去法开篇），被视为"完美的教学伴侣"，但在深度和全面性上，《矩阵计算》仍是不可替代的。

在软件层面，该书直接影响了 LAPACK（1992年起）和 ScaLAPACK（分布式并行版本）的设计。LAPACK 作为 LINPACK 和 EISPACK 的现代继承者，采用分块算法（Level 3 BLAS）来适应多层次存储结构，其算法选择和实现方案在很大程度上参考了《矩阵计算》的分析。而 MATLAB 自2000年起将其底层线性代数计算迁移到 LAPACK，意味着全球数以百万计的 MATLAB 用户每天都在间接使用本书描述的算法。

---

## 解决了什么瓶颈

1983年之前，一个研究生若要全面了解矩阵计算，需要阅读 Wilkinson 的 *The Algebraic Eigenvalue Problem*（1965，侧重特征值和误差分析）、Stewart 的 *Introduction to Matrix Computations*（1973，侧重教学但范围有限）、Wilkinson-Reinsch 的 *Handbook*（1971，侧重算法实现但缺乏理论背景）以及散布在 *Numerische Mathematik*、*SIAM Journal on Numerical Analysis* 等期刊上的大量论文。这些文献在符号体系、算法描述风格和分析深度上都不统一，给学习者和实践者造成了巨大障碍。

《矩阵计算》用一种统一的框架——矩阵分解、伪代码描述、向后误差分析——将全部内容重新组织，消除了知识碎片化的瓶颈。Nick Higham 在回忆中特别提到，本书最令人兴奋的特点之一是"对共轭梯度法和 Lanczos 方法的系统处理"，这些内容在此前的教科书中几乎找不到。此外，本书首次在教科书层面系统讨论了广义 SVD、全最小二乘（Total Least Squares）和条件数估计等前沿主题。

更深层的瓶颈在于"表述方式"的标准化。在本书之前，不同作者使用不同的符号体系、不同的矩阵索引约定、不同的误差度量标准来描述同一个算法，这使得跨文献的比较和学习变得异常困难。Golub 和 Van Loan 引入的 MATLAB 风格伪代码（使用冒号记号表示矩阵切片，如 $A(i\text{:}j, k\text{:}l)$）极大地简化了算法描述，成为后续几乎所有数值分析教科书的标准写法。这种符号上的统一看似微小，实际上降低了整个学科的入门门槛和交流成本，其影响远远超出了一本书的范畴。

---

## 与前人工作的关系

本书明确继承并整合了以下学术传统：

**Wilkinson 的误差分析传统**。Wilkinson 1965年建立的向后误差分析框架是本书所有稳定性讨论的理论基础。Golub 本人曾表示，他的学术志向是"将 Wilkinson 的教训应用到不同的应用领域中"。

**Householder 的正交化方法**。Alston S. Householder 在1958年提出的反射变换（Householder reflections）为 QR 分解提供了数值稳定的基本工具。本书将这一方法提升到中心地位，视其为正交分解的首选手段。

**Stewart 的教科书传统**。G. W. Stewart 1973年的 *Introduction to Matrix Computations* 是第一部现代风格的矩阵计算教科书。Golub-Van Loan 在致谢中承认了这一影响，但在深度、广度和前沿性上进行了全面超越。

**Lanczos 的迭代方法**。Cornelius Lanczos 在1950年代提出的三对角化迭代为大规模特征值计算提供了理论框架，但长期被认为在实践中不可靠（因为有限精度下的正交性损失）。Golub 及其合作者（特别是 Paige）的工作澄清了 Lanczos 算法的数值行为，本书对这些结果的系统阐述极大地推动了 Lanczos 方法的实际应用。

**Golub 自己的 SVD 工作**。Golub 与 Kahan 1965年以及与 Reinsch 1970年的合作直接为本书的 SVD 章节提供了核心内容。Van Loan 则在全最小二乘、Kronecker 积计算和矩阵指数函数等方面贡献了重要的原创内容。

---

## 对后续工作的影响

本书的影响辐射到了数值线性代数的每一个分支以及更广泛的计算科学领域：

**软件库**。LAPACK（Linear Algebra PACKage）直接以本书描述的算法为蓝本，通过引入 Level 3 BLAS 实现了对缓存层次结构的高效利用。ScaLAPACK 将这些算法扩展到分布式存储系统。MATLAB 在2000年全面采用 LAPACK 作为底层引擎。可以毫不夸张地说，本书间接决定了当代科学计算软件的核心算法选择。

**教材**。Trefethen 和 Bau 的 *Numerical Linear Algebra*（1997）被明确定位为本书的"教学伴侣"，采用更适合课堂的讲座式组织。Demmel 的 *Applied Numerical Linear Algebra*（1997）也在很大程度上以本书为参考框架。

**深度学习基础设施**。PyTorch、TensorFlow 等现代深度学习框架的底层线性代数运算依赖 cuBLAS、cuSOLVER 等 GPU 加速库，而这些库所实现的算法——矩阵乘法优化、QR 分解、SVD 等——其算法设计仍然可以追溯到本书的描述。

**数据科学**。SVD 和低秩矩阵近似在推荐系统（如 Netflix Prize 竞赛中的矩阵分解方法）、主成分分析（PCA）和潜在语义分析（LSA）中的广泛应用，使得本书中的经典算法获得了全新的应用场景。

**学术传承**。Golub 在 Stanford 培养了众多学生和博士后，他们分散到世界各地的大学和研究机构，将《矩阵计算》的知识体系和研究风格进一步传播。Van Loan 在 Cornell 同样培养了大量优秀人才。两位作者通过这本书建立的学术标准——算法设计必须伴随严格的误差分析，理论结果必须转化为可执行的伪代码——已经成为数值计算领域的基本规范。可以说，当代数值分析研究者的思维方式在很大程度上被这本书塑造了。

---

## 现代价值

尽管第1版出版已逾四十年，《矩阵计算》在当代计算科学中仍具有不可替代的参考价值：

**大规模机器学习**。SVD 在推荐系统中的应用（矩阵分解方法）、PCA 在高维数据降维中的应用、以及随机化线性代数（randomized numerical linear algebra）的兴起，都以本书的经典理论为基石。第4版新增的大规模稀疏 SVD 和 Krylov 子空间方法章节直接回应了这些需求。

**GPU 加速科学计算**。NVIDIA 的 cuSOLVER 库实现了本书描述的 LU、QR、Cholesky、SVD 等分解的 GPU 并行版本。理解这些算法的数据依赖关系和数值稳定性——正是本书所提供的——对于高效的 GPU 实现至关重要。

**量子计算模拟**。量子线路模拟需要处理指数级增长的复数矩阵，其中 Schmidt 分解（SVD 的物理对应）和矩阵指数函数（第4版专设章节）是核心工具。

**张量计算**。第4版新增的 Kronecker 积计算、张量展开和张量分解章节反映了这一快速发展的前沿方向，直接关联到信号处理、化学计量学和深度学习中的张量网络方法。

**数值稳定性教育**。在当代机器学习实践中，混合精度训练（mixed-precision training）、低精度推理（INT8/FP16 quantization）等技术的广泛应用，使得浮点算术误差分析重新获得关注。本书对浮点运算模型、舍入误差传播和数值稳定性的系统讨论，为理解这些现代技术的理论基础提供了不可替代的参考。许多深度学习研究者在遇到训练不稳定问题时，最终都会回到本书的条件数和误差分析章节寻找答案。

**跨学科桥梁**。《矩阵计算》的另一个现代价值在于它为不同学科的研究者提供了共同的技术语言。无论是物理学家模拟量子系统、经济学家求解均衡模型、生物学家分析基因表达数据，还是工程师设计控制系统，他们所使用的核心数值方法都可以在这本书中找到统一的描述。这种跨学科的统一性在当今日益强调学科交叉的学术环境中显得尤为珍贵。

---

## 通俗解读

如果将数值线性代数比作建筑工程，那么《矩阵计算》就是这个行业最权威的"工具箱手册"。

想象你是一名建筑工程师，面前有各种各样的施工任务：打地基（求解线性方程组）、测量结构承重能力（计算特征值）、检测建筑变形（奇异值分解）、调整设计参数（最小二乘拟合）。对于每种任务，这本"手册"不仅告诉你应该用什么工具（选择哪种算法），还告诉你每种工具的精度有多高（误差分析）、在什么条件下可能失效（数值稳定性）、以及与其他工具相比的优劣（算法复杂度对比）。

更妙的是，所有工具都按照一个统一的原理组织：先将复杂结构拆解为简单组件（矩阵分解），再利用简单组件解决实际问题。这就像先将建筑拆解为梁、柱、板等标准构件，再按需组装。LU 分解是最基础的拆解方式，QR 分解是更精密的正交拆解，而 SVD 则是终极拆解——它揭示了结构的全部几何信息。

这本手册之所以几十年来无人能替代，是因为它在全面性、深度和实用性之间达到了罕见的平衡。你可以在科研中查阅某个算法的误差界，也可以在工程实践中据此选择合适的软件库函数。

再换一个比喻：如果数学是一座大厦，线性代数就是它的钢筋骨架，而《矩阵计算》就是教你如何在计算机上精确、高效地建造这副骨架的施工指南。从桥梁工程到天气预报，从搜索引擎排序到手机拍照的图像处理，几乎所有需要大规模数值计算的领域，都离不开矩阵运算。当你在手机上刷短视频，推荐系统背后的核心算法之一就是本书详细讲解的"奇异值分解"；当你使用语音助手，语音识别模型训练时求解的大规模线性方程组，其底层算法同样来自这本书。可以说，《矩阵计算》虽然看起来是一本数学专著，但它所描述的算法早已默默渗透到现代数字生活的每一个角落。

---

## 阅读指南

**入门路径**（适合初次接触数值线性代数的研究生）：建议先阅读 Trefethen-Bau 的 *Numerical Linear Algebra* 建立直觉，再以《矩阵计算》为深入参考。在本书内部，推荐按以下顺序阅读：

1. 第1章（矩阵乘法）：建立算法分析的基本框架和 flop 计数思维
2. 第2章（矩阵分析）：掌握范数、SVD 理论和条件数概念
3. 第3章（一般线性方程组）：理解 LU 分解和 Gaussian 消去法
4. 第5章（正交化与最小二乘）：掌握 QR 分解和 Householder/Givens 变换
5. 第8章（对称特征值问题）：SVD 的计算算法

**进阶路径**（适合已有基础的研究人员）：直接查阅感兴趣的章节。第4版每章开头列出了该章涉及的关键主题和相关的全局参考文献（Global References），便于定位。

**工程师快速参考**：如果只需了解如何为特定问题选择合适的算法和软件，可以先阅读相关章节的引言和算法伪代码，再查看对应的 LAPACK 子程序名称。

**不推荐**的阅读方式：从头到尾顺序通读。本书近800页，内容密度极高，更适合作为参考书按需查阅。

**版本选择建议**：如果只购买一个版本，推荐第4版（2013），因为它在保留经典内容的同时大幅扩充了现代主题。但如果能找到第3版（1996），它在某些方面更为简洁，且附有每章对应的 LAPACK 子程序列表，对工程实践者非常方便。第1版和第2版主要具有收藏和历史研究价值。

**搭配阅读建议**：建议与 Higham 的 *Accuracy and Stability of Numerical Algorithms* 配合使用——前者侧重算法设计和复杂度分析，后者侧重误差分析的技术细节，两者互为补充。对于需要实际编程的读者，LAPACK Users' Guide 是必不可少的配套参考，它将本书的伪代码与可调用的 Fortran 子程序一一对应。

---

## 局限性

**稠密矩阵偏向**。前三版的重心明显偏向稠密矩阵的直接方法，对稀疏矩阵的处理相对简略。虽然第4版增加了稀疏直接方法、多重网格和预处理等章节，但相比 Timothy Davis 的 *Direct Methods for Sparse Linear Systems*（2006）等专著仍显不足。

**并行计算覆盖有限**。尽管第4版增加了并行 LU 和并行矩阵乘法的讨论，但对 GPU 计算、分布式计算和异构架构上的矩阵算法的覆盖仍然有限。这与本书出版周期较长（版次间隔16--17年）有关。

**随机化算法的缺席**。随机化数值线性代数（randomized NLA）是过去十五年最活跃的研究方向之一，以 Halko-Martinsson-Tropp 2011年的综述论文为标志。第4版（2013）仅有零星提及，未做系统处理。

**概率分析视角的不足**。本书遵循 Wilkinson 的确定性误差分析传统，对近年来兴起的概率舍入误差分析（如 Higham-Mary 2019年的工作）尚未涉及。

**实现细节与硬件映射**。书中以伪代码描述算法，但未深入讨论实际实现中的缓存优化、向量化和 SIMD 指令利用等问题。这些内容需要参考 Dongarra 等人的专门文献。

**第5版的缺席**。Golub 于2007年去世后，Van Loan 独自完成了第4版的修订工作，并在序言中表达了深切的遗憾。截至目前，尚无第5版的出版计划。考虑到数值线性代数在过去十年的迅速发展——随机化算法、通信避免算法（communication-avoiding algorithms）、混合精度计算、张量网络方法等——一部新版本的需求日益迫切。然而，能否找到一位或几位作者来承担这一巨大的更新任务，是一个尚待解决的问题。这也从侧面反映了 Golub 和 Van Loan 的原著所达到的高度：它的全面性和权威性使任何更新都成为一项艰巨的挑战。

---

## 延伸阅读

1. **Wilkinson, J. H.** *The Algebraic Eigenvalue Problem*. Oxford: Clarendon Press, 1965. -- 特征值计算和误差分析的奠基之作，Golub-Van Loan 书中误差分析传统的直接源头。

2. **Stewart, G. W.** *Introduction to Matrix Computations*. New York: Academic Press, 1973. -- 第一部现代风格的矩阵计算教科书，Golub-Van Loan 的直接前驱。

3. **Trefethen, L. N. & Bau, D.** *Numerical Linear Algebra*. Philadelphia: SIAM, 1997. -- 以40个讲座组织的教学杰作，被称为《矩阵计算》的"完美教学伴侣"。

4. **Demmel, J. W.** *Applied Numerical Linear Algebra*. Philadelphia: SIAM, 1997. -- 更侧重应用和扰动理论，对并行计算有更多讨论。

5. **Higham, N. J.** *Accuracy and Stability of Numerical Algorithms*. 2nd ed. Philadelphia: SIAM, 2002. -- 舍入误差分析的现代百科全书，深化了 Wilkinson-Golub 的误差分析传统。

6. **Davis, T. A.** *Direct Methods for Sparse Linear Systems*. Philadelphia: SIAM, 2006. -- 填补了《矩阵计算》在稀疏直接方法方面的不足。

7. **Halko, N., Martinsson, P. G., & Tropp, J. A.** "Finding Structure with Randomness: Probabilistic Algorithms for Constructing Approximate Matrix Decompositions." *SIAM Review*, 53(2):217--288, 2011. -- 随机化数值线性代数的里程碑综述，代表了《矩阵计算》未来版本可能需要大幅扩充的方向。

8. **Dongarra, J. J. et al.** *LAPACK Users' Guide*. 3rd ed. Philadelphia: SIAM, 1999. -- 《矩阵计算》所描述算法的工业级实现手册，是理论与实践之间的桥梁。

---

## 参考文献

1. Golub, G. H. & Van Loan, C. F. *Matrix Computations*. 1st ed. Baltimore: Johns Hopkins University Press, 1983. 476 pp. ISBN 978-0-8018-3010-8.

2. Golub, G. H. & Van Loan, C. F. *Matrix Computations*. 2nd ed. Baltimore: Johns Hopkins University Press, 1989. 642 pp. ISBN 978-0-8018-3772-5.

3. Golub, G. H. & Van Loan, C. F. *Matrix Computations*. 3rd ed. Baltimore: Johns Hopkins University Press, 1996. 694 pp. ISBN 978-0-8018-5414-9.

4. Golub, G. H. & Van Loan, C. F. *Matrix Computations*. 4th ed. Baltimore: Johns Hopkins University Press, 2013. 756 pp. ISBN 978-1-4214-0794-4.

5. Golub, G. H. & Kahan, W. "Calculating the Singular Values and Pseudo-Inverse of a Matrix." *J. SIAM Ser. B Numer. Anal.*, 2(2):205--224, 1965.

6. Golub, G. H. & Reinsch, C. "Singular Value Decomposition and Least Squares Solutions." *Numer. Math.*, 14(5):403--420, 1970.

7. Wilkinson, J. H. *The Algebraic Eigenvalue Problem*. Oxford: Clarendon Press, 1965.

8. Stewart, G. W. *Introduction to Matrix Computations*. New York: Academic Press, 1973.

9. Wilkinson, J. H. & Reinsch, C. (eds.) *Handbook for Automatic Computation, Volume II: Linear Algebra*. Berlin: Springer-Verlag, 1971.

10. Dongarra, J. J., Bunch, J. R., Moler, C. B., & Stewart, G. W. *LINPACK Users' Guide*. Philadelphia: SIAM, 1979.

11. Higham, N. J. "Fourth Edition (2013) of Golub and Van Loan's Matrix Computations." Blog post, May 31, 2013.

12. Greif, C. "Gene H. Golub Biography." Stanford University ICME Archives.

13. Trefethen, L. N. & Bau, D. *Numerical Linear Algebra*. Philadelphia: SIAM, 1997.
