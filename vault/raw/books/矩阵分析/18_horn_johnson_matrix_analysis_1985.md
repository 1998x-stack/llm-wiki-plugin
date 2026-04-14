# Horn--Johnson《矩阵分析》（1985）：矩阵理论的现代综合

---

## 1. 作者

**Roger A. Horn**（罗杰·霍恩，1942--）与 **Charles R. Johnson**（查尔斯·约翰逊，1948--）。

Horn 于 1942 年 1 月 19 日出生，1963 年以优异成绩毕业于 Cornell University 数学系，1967 年在 Stanford University 取得博士学位，师从 Charles Loewner 与 Donald C. Spencer，博士论文研究无穷可分矩阵（infinitely divisible matrices）。1968 年起任教于 Johns Hopkins University 数学系，并于 1972 至 1979 年间创建并担任该校数理科学系主任。在此期间，他组织了一系列短期课程讲座，并邀请 Gene Golub 与 Charles Van Loan 撰写专著，后来发展为经典教材 *Matrix Computations*。Horn 后转至 University of Utah 担任数学研究教授，2015 年退休。除矩阵分析外，他还与 Paul T. Bateman 共同提出了关于多项式素数值密度的 Bateman--Horn 猜想。

Johnson 于 1948 年 1 月 28 日出生，1969 年在 Northwestern University 获得数学与经济学学士学位（优等），1972 年在 California Institute of Technology 获博士学位，导师为著名矩阵理论家 Olga Taussky-Todd，博士论文题为"Matrices whose Hermitian Part is Positive Definite"。此后他在 University of Maryland 任教十年（1974--1984），又在 Clemson University 短暂任职（1984--1987），最终于 1987 年加入 College of William & Mary 数学系，担任"Class of 1961"讲座教授，直至 2024 年。Johnson 的研究兴趣涵盖非负逆特征值问题（NIEP）、完成问题（completion problems）、谱图理论和随机矩阵等广泛领域。

两位作者的合作始于 1970 年代末。Horn 深厚的分析功底与 Johnson 在组合矩阵论方面的专长形成互补，使得他们能够从不同视角整合矩阵分析的核心成果。

---

## 2. 发表时间与出版信息

本书初版由 Cambridge University Press 于 **1985 年** 出版，精装本共 XIII + 561 页，ISBN 0-521-30586-1。1990 年推出平装版。**第二版**于 **2013 年** 出版，页数增至 643 页，习题从约 690 道扩展至 1100 余道，索引条目从约 1200 条增至 3500 余条。第二版增加了奇异值分解与 CS 分解的新章节、Weyr 标准形、Jordan 标准形的新应用，并大幅扩展了分块矩阵和逆问题的讨论。

---

## 3. 一句话概括

**首次将矩阵分析作为独立数学学科进行系统性综合，以矩阵分解为主线、以不等式为核心工具，涵盖特征值理论、范数理论、正定性与特殊矩阵，为此后四十年的教学与研究确立了标准范式。**

---

## 4. 历史背景

矩阵理论的历史可以追溯到 19 世纪 Arthur Cayley 和 James Joseph Sylvester 的开创性工作，但在 20 世纪大部分时间里，矩阵的深层分析结果一直散落在纯数学、应用数学、物理学、统计学和工程学的各个领域中，没有形成统一的学科体系。1950 年代至 1970 年代，矩阵理论的地位相当尴尬：它既不完全属于抽象代数（后者更关注一般线性空间和模理论），也不完全属于数值分析（后者更关注计算效率），而是一个介于理论与应用之间的"灰色地带"。

在这一时期，已有若干重要的矩阵理论著作问世。苏联数学家 F. R. Gantmacher 的两卷本 *The Theory of Matrices*（1959 年英译本）是一部百科全书式的巨著，以经典代数方法处理矩阵的标准形、多项式矩阵和初等因子理论，但其风格偏重代数结构，对分析工具（如范数和不等式）着墨较少。Richard Bellman 的 *Introduction to Matrix Analysis*（1960 年初版）首次在英语文献中将对称矩阵与二次型、矩阵微分方程、正矩阵与概率论三个领域统一论述，但其覆盖面有限且带有浓厚的应用倾向。Marvin Marcus 与 Henryk Minc 合著的 *A Survey of Matrix Theory and Matrix Inequalities*（1964）以简洁的方式综述了矩阵不等式的经典结果，但篇幅仅 180 页，更像是一份导引而非系统教材。

到了 1980 年代初，矩阵分析面临一个关键转折点。一方面，数值线性代数在 Golub 和 Van Loan 的推动下已发展为成熟学科（*Matrix Computations* 于 1983 年出版）；另一方面，矩阵不等式和结构化矩阵的理论结果在控制论、统计学和优化理论中的应用日益广泛。然而，研究生和青年学者要学习矩阵分析的核心内容，却不得不从数十种期刊论文和各种专著中拼凑知识。Horn 在 Johns Hopkins 的教学经历使他深刻感受到这一知识碎片化问题：线性代数的基础课程教授向量空间和线性变换的一般理论，但从 Schur 三角化到 Weyl 特征值不等式的大量深层结果却无处可学。

正是在这一背景下，Horn 与 Johnson 决定合作撰写一部系统化的矩阵分析教材。Horn 提供了分析学视角和在 Johns Hopkins 多年积累的教学经验，Johnson 则带来了组合矩阵论和正矩阵方面的深厚功底。两人花费数年时间，将散落在 250 年数学文献中的矩阵分析核心结果组织成一个连贯的、层层递进的理论体系，最终于 1985 年由 Cambridge University Press 出版。这部著作的出现标志着"矩阵分析"（matrix analysis）从线性代数的一个附属分支正式成为一个独立的、有明确边界和方法论的数学学科。

---

## 5. 核心问题

本书试图回答一个根本性的学科建设问题：**如何将 250 年来矩阵分析的核心结果——从 Cayley 和 Sylvester 的 19 世纪工作到 20 世纪下半叶的最新成果——组织成一个连贯的、可教学的、逻辑自洽的理论体系？** 具体而言，作者需要解决三个层面的挑战：第一，如何选择和组织主题，使得一本教材既能覆盖矩阵分析的核心内容，又不至于沦为一份庞杂的结果列表；第二，如何找到一条贯穿全书的主线，将看似不相关的主题（特征值不等式、矩阵范数、正定性、非负矩阵）联系起来；第三，如何在严格的数学论证与可读性之间找到平衡，使得这本书既能作为研究生教材，又能作为研究者的参考手册。

这一核心问题的难度不应被低估。矩阵分析横跨纯数学与应用数学的边界，涉及代数、分析、几何和组合等多个分支，其结果的表述风格和证明技巧差异极大。将这些异质性极强的材料融合为一个有机整体，需要作者对整个领域具有全景式的把握和深刻的审美判断力。Horn 和 Johnson 给出的答案是以"标准形"（canonical form）作为统一框架：每一章对应一类矩阵等价关系及其标准形，由此自然引出该等价关系下的不变量、不等式和应用。这一组织策略既忠实于矩阵理论的内在逻辑，又为教学提供了清晰的路径。

---

## 6. 主要定理与结果

本书的核心内容可以沿以下几条主线展开：

**（一）矩阵标准形与分解理论。** 全书以矩阵分解为组织框架。Schur 三角化定理（任何复方矩阵酉相似于上三角矩阵）是全书的起点和基石。在此基础上，书中系统发展了 Jordan 标准形、实 Schur 形式，以及正规矩阵的谱定理。第二版进一步加入了 Weyr 标准形和 CS 分解。三种基本的相似关系——一般相似（similarity）、酉相似（unitary similarity）和合同（congruence）——贯穿全书，为不同类型的矩阵分析提供了统一框架。

**（二）Hermite 矩阵特征值不等式。** 这是全书最具深度的部分之一。作者系统阐述了 Hermann Weyl（1912）关于 Hermite 矩阵之和的特征值不等式、Ky Fan（1949）的推广（特征值部分和的优超关系）、以及 Lidskii（1950）的更一般结果。这些不等式揭示了 Hermite 矩阵特征值在矩阵加法下的精细行为，构成了矩阵扰动理论的基础。书中还讨论了 Cauchy 交错定理和 Courant-Fischer 极小极大原理，将这些表面上不同的结果统一在一个优超（majorization）理论的框架下。

**（三）奇异值理论。** 奇异值分解（SVD）在第二版中被提前至更显著的位置。书中建立了奇异值与特征值之间的深刻联系，证明了奇异值不等式（包括乘积型不等式），并讨论了 SVD 在矩阵逼近、低秩近似和极分解中的应用。Von Neumann 迹定理在第二版中被赋予了核心地位。

**（四）矩阵范数理论。** 作者建立了矩阵范数的完整理论，包括算子范数（由向量范数诱导）、酉不变范数（Ky Fan 范数、Schatten 范数）和 Frobenius 范数。范数理论将矩阵分析与泛函分析联系起来，为扰动理论和收敛性分析提供了基本工具。

**（五）正定矩阵与合同理论。** Hermite 正定矩阵的理论是全书的重要支柱。作者讨论了正定性的等价刻画（Sylvester 准则、特征值判据、Cholesky 分解）、正定矩阵锥的几何性质、以及矩阵合同关系下的不变量。Loewner 偏序和矩阵单调函数的理论也有涉及。

**（六）非负矩阵与 M-矩阵。** 最后一章系统阐述了 Perron-Frobenius 理论：非负不可约矩阵存在正的最大特征值（Perron 根），对应正的特征向量。书中还讨论了 M-矩阵（对角占优矩阵的推广）、随机矩阵和双随机矩阵的基本性质。Birkhoff 定理（双随机矩阵是置换矩阵的凸组合）与 Perron-Frobenius 定理的结合，为 Markov 链的收敛性分析提供了完整的理论基础。这一章也为 Johnson 后来在非负逆特征值问题（NIEP）上的深入研究埋下了伏笔。

**（七）特征值定位与 Gershgorin 圆盘。** 书中详细阐述了 Gershgorin 圆盘定理及其各种推广，提供了仅通过矩阵元素即可估计特征值位置的有力工具。这些定位结果在数值分析中特别有用，它们为迭代算法的收敛性分析和矩阵谱的粗略估计提供了理论保障。

---

## 7. 核心方法

本书的方法论可以概括为"分解--不等式--结构"三位一体。

**以矩阵分解为主线**：不同类型的分解对应不同的等价关系（相似、酉相似、合同），而每一类等价关系下的标准形揭示了矩阵的本质结构。这一视角使得看似不同的主题（如特征值理论和正定性理论）通过不同的分解类型得到统一。

**以不等式为核心工具**：矩阵分析区别于抽象线性代数的关键特征在于它对"量"的关注——不仅关心矩阵的代数结构，更关心特征值的大小关系、范数的界和扰动的量化估计。Weyl 不等式、Ky Fan 不等式、Lidskii 不等式以及各种范数不等式构成了全书的分析骨架。

**强调结构化矩阵类的特殊性质**：Hermite 矩阵、正定矩阵、正规矩阵、非负矩阵——这些具有特殊结构的矩阵类在应用中反复出现，而它们各自拥有远比一般矩阵更丰富、更精细的理论。作者的策略是先建立一般理论，再逐步特化到这些重要的矩阵类，展示结构化假设如何带来更强的结论。

---

## 8. 重要性与影响

《矩阵分析》自出版以来已成为矩阵理论领域被引用最多的著作之一。据 Semantic Scholar 统计，本书累计被引用超过 **26,000 次**，其中高影响力引用超过 2,100 次。Roger Horn 的 Google Scholar 主页显示其个人总引用量近 69,000 次，其中本书贡献了绝大部分。在数学教材中，如此高的引用量极为罕见，反映了本书跨学科的深远影响。

本书的影响首先体现在**学科定义**层面。在本书出版之前，"矩阵分析"这一术语虽然偶有使用，但并无公认的学科边界。Horn 和 Johnson 通过精心选择和组织主题，事实上定义了矩阵分析作为一个独立学科的范围和方法论：它以有限维线性代数为起点，以分解理论和不等式为核心工具，以结构化矩阵类的深层性质为研究对象。此后，全球众多大学开设的"矩阵分析"课程基本上都以本书为蓝本。

本书的影响其次体现在**研究范式**层面。它为后续研究者提供了统一的术语体系、标准的记号约定和规范的证明风格。在本书出版之前，同一个定理在不同文献中可能有完全不同的表述方式；本书确立的标准化表述被广泛采纳，成为数学共同体的"共同语言"。

本书还深刻影响了**跨学科应用**。控制理论家用它来分析系统的稳定性，统计学家用它来处理协方差矩阵，物理学家用它来研究量子力学中的算子理论，计算机科学家用它来理解机器学习中的矩阵优化。Ilse Ipsen 评价第二版为"对广受欢迎的第一版的重大提升"，称其为"矩阵理论与应用的里程碑式贡献"；也有评论者称之为"矩阵分析基础的权威来源和不可替代的参考文献"。

2007 年，*Linear Algebra and its Applications* 杂志出版了专门献给 Horn 的特刊（Volume 424, Issue 1），以表彰他对矩阵分析的奠基性贡献。

---

## 9. 解决了什么瓶颈

在本书出版之前，矩阵分析领域存在严重的**知识碎片化**问题。一个典型的例子是 Hermite 矩阵的特征值不等式：Weyl 的原始结果发表于 1912 年的德语论文中，Ky Fan 的推广发表于 1949 年的 *Proceedings of the National Academy of Sciences*，Lidskii 的工作发表于 1950 年的苏联科学院通报——要全面了解这一主题，研究者需要阅读跨越近 40 年、分布在至少三种语言文献中的原始论文。

类似的碎片化存在于矩阵范数理论、正定矩阵、非负矩阵等几乎所有子主题中。研究生想要系统学习矩阵分析，只能依赖导师的个人传授或自行从海量文献中拼凑知识。Horn 和 Johnson 的贡献在于，他们首次将这些散落的结果收集、整理、统一表述，并构建了一个内在逻辑连贯的知识体系。

---

## 10. 与前人工作的关系

本书的学术谱系可以通过与四部前驱著作的对比来理解。

**Gantmacher《矩阵论》（1959 年英译本）**：这是苏联学派矩阵理论的集大成之作，两卷本共计近千页，以代数方法系统处理了矩阵标准形、多项式矩阵、初等因子和 Jordan 理论。Gantmacher 的风格偏重代数结构，对分析工具（范数、不等式、扰动理论）涉及较少。Horn--Johnson 的工作可以看作是将 Gantmacher 的代数视角与西方学派的分析视角相融合。

**Bellman《矩阵分析导引》（1960）**：Bellman 的贡献在于首次在英语教材中统一论述了对称矩阵与二次型、矩阵微分方程、正矩阵与概率论，但其覆盖面有选择性，且倾向于动力系统和控制论的应用。Horn--Johnson 的范围更广，理论性更强。

**Marcus--Minc《矩阵论与矩阵不等式概览》（1964）**：这是一份精简的综述（180 页），以矩阵不等式和组合矩阵论为重点，涵盖了 Kronecker 积、永久式（permanent）、Perron-Frobenius 理论等主题。其组合视角对 Johnson 的研究有重要影响，但篇幅限制使其无法提供完整的理论发展。

**Golub--Van Loan《矩阵计算》（1983）**：这部由 Horn 在 Johns Hopkins 促成的经典教材从计算和算法的角度处理矩阵问题。Horn--Johnson 与 Golub--Van Loan 构成了矩阵理论的两大支柱：前者侧重理论分析，后者侧重数值计算；两者互为补充，缺一不可。

值得一提的是，Johnson 的博士导师 Olga Taussky-Todd 是 20 世纪矩阵论的核心人物之一，她对正定矩阵、矩阵合同和代数数论中的矩阵问题的研究深刻影响了 Johnson 的学术品味，也在本书中留下了清晰的印记。

---

## 11. 对后续工作的影响

本书直接催生了一系列后续著作，形成了矩阵分析文献的"生态系统"。

**Horn--Johnson《矩阵分析中的论题》（1991）**：作为直接续篇，这部 607 页的专著讨论了第一本书未涵盖的深层主题，包括数值域（field of values）、矩阵稳定性与惯性（Lyapunov 定理）、奇异值的进一步理论、Kronecker 积与矩阵方程、Hadamard 积（Schur 乘积定理及其推广）以及矩阵函数。两本书合在一起构成了矩阵分析的完整参考体系。

**Rajendra Bhatia《矩阵分析》（1997，Springer GTM 169）**：Bhatia 在 Horn--Johnson 的基础上进一步深化，特别是在优超理论（majorization）、特征值变分原理、算子单调和算子凸函数、以及矩阵函数的扰动理论方面做出了重要推进。该书被 Zentralblatt Math 评为"矩阵分析领域的必读之作"，已被引用超过 7,800 次。

**中国矩阵论教材**：在中国，张贤达《矩阵分析与应用》等教材在很大程度上受到 Horn--Johnson 体系的影响，将其核心框架引入中文教学。北京大学、清华大学等高校的矩阵分析课程普遍采用 Horn--Johnson 作为主要参考文献。

本书还深刻影响了矩阵理论的几个专门研究方向。非负矩阵逆特征值问题（NIEP）——这是 Johnson 自己的长期研究课题——受到本书对 Perron-Frobenius 理论系统阐述的推动。矩阵完成问题（completion problems）的现代研究也与本书建立的正定性理论密切相关。

---

## 12. 现代价值

在本书出版近四十年后的今天，其核心内容的重要性不减反增，在多个前沿领域发挥着基础性作用。

**数据科学与机器学习**：主成分分析（PCA）的数学基础就是奇异值分解和特征值不等式。矩阵范数理论是理解正则化方法（如核范数最小化）的关键。低秩矩阵近似（Eckart--Young 定理）在推荐系统和自然语言处理中广泛应用。

**量子信息与量子计算**：量子态由密度矩阵（正半定、迹为 1 的 Hermite 矩阵）描述，量子操作由酉矩阵表示。本书关于正定矩阵和酉相似的理论直接构成量子信息理论的数学基础。

**控制理论与系统工程**：线性系统的稳定性分析依赖于矩阵特征值的定位，Lyapunov 矩阵方程的可解性与矩阵惯性理论密切相关。

**优化理论**：半定规划（SDP）的理论基础建立在正半定矩阵锥的几何性质之上，而凸优化中的矩阵不等式（线性矩阵不等式，LMI）正是本书所建立的理论的直接应用。

**统计学与多元分析**：协方差矩阵的正定性、Wishart 分布的特征值分布、Fisher 信息矩阵——这些统计学的核心概念都需要本书提供的矩阵分析工具。

**信号处理与通信**：多天线系统（MIMO）的容量分析本质上是一个矩阵特征值问题，信道矩阵的奇异值决定了系统的最大传输速率。波束成形（beamforming）算法依赖 Hermite 矩阵的谱分解，而信号子空间方法（MUSIC、ESPRIT）的理论基础也植根于本书所建立的矩阵分析框架。

**网络科学与图论**：图的邻接矩阵和 Laplacian 矩阵的谱性质揭示了网络的连通性、社区结构和扩散行为。Google 的 PageRank 算法本质上是一个非负矩阵的 Perron 向量计算问题，其理论根基正是本书最后一章所阐述的 Perron-Frobenius 理论。

---

## 13. 通俗解读

理解本书的定位，可以借助一个"百科全书与教科书"的比喻。在 Horn--Johnson 之前，矩阵分析的知识像一座没有目录、没有索引的巨大图书馆——珍贵的文献确实存在，但分散在无数书架上，只有资深馆员（即经验丰富的研究者）才能找到需要的内容。Gantmacher 的著作像一部俄文百科全书，包罗万象但不适合按部就班地学习；Bellman 的著作像一份精心编排的旅行指南，内容精彩但只覆盖了作者个人偏好的几条路线。

Horn 和 Johnson 所做的工作，相当于为这座图书馆建造了一套完整的目录系统：他们不仅收集和分类了馆藏，更重要的是设计了一条从入门到精通的参观路线——读者可以从 Schur 三角化这个"入口大厅"出发，沿着特征值理论、范数理论、正定性的路径，最终到达非负矩阵的"深层展厅"。每一站之间都有清晰的逻辑连接，使得整个旅程既有深度又不失连贯。

还可以用另一种方式理解本书的价值。假设一位工程师需要分析一个线性系统的稳定性，他知道这与矩阵特征值有关，但不知道如何精确估计特征值的位置。在 Horn--Johnson 之前，他可能需要辗转查找 Gershgorin 的原始论文（1931 年俄语发表）、Brauer 的改进（1947）和 Varga 的推广（1962），然后自己拼凑出一套可用的理论。有了 Horn--Johnson，他只需翻到相应章节，就能找到从基本定理到最新推广的完整论述，以及精心设计的习题来帮助巩固理解。这种"一站式"的知识获取体验，正是本书持久受欢迎的根本原因。

---

## 14. 阅读指南

对于不同背景的读者，建议以下阅读路径。

**研究生初学者**：按章节顺序阅读。第 1 章（特征值、特征向量和相似性）和第 2 章（酉相似和酉等价）是全书的基础，必须扎实掌握。建议认真完成每章的习题——第二版提供了超过 1100 道习题及附录提示，是巩固理解的最佳途径。

**应用领域研究者（工程、统计、物理）**：可以优先阅读第 4 章（Hermite 矩阵和对称矩阵）、第 5 章（范数）和第 7 章（正定矩阵），这三章提供了应用中最常用的工具。非负矩阵章节对于处理 Markov 链和图论问题的读者同样重要。

**有经验的数学家**：可将本书作为参考手册使用。第二版极其详尽的 37 页索引（3500+ 条目）使得快速查找特定结果变得非常方便。

**配合续篇阅读**：在掌握本书内容后，可继续阅读 *Topics in Matrix Analysis*（1991），特别是数值域（第 1 章）、Hadamard 积（第 5 章）和矩阵函数（第 6 章）等在本书中未详细展开的主题。Bhatia 1997 年的 *Matrix Analysis* 则提供了更深入的扰动理论和优超理论视角。

**预备知识建议**：阅读本书之前，读者应具备一学期的线性代数基础，包括向量空间、线性变换、行列式和特征值的基本概念。Horn 与 Garcia 合著的 *Matrix Mathematics: A Second Course in Linear Algebra*（2nd ed., 2023）可作为理想的预备读物，帮助读者弥合初等线性代数课程与本书之间的知识鸿沟。对于中国读者，北京大学或清华大学的高等代数教材（如丘维声《高等代数》或蓝以中《高等代数简明教程》）提供了足够的预备知识。

---

## 15. 局限性

尽管本书的学术地位毋庸置疑，但也存在若干值得注意的局限。

**计算方法覆盖不足**：本书几乎完全聚焦于理论分析，对计算算法（如 QR 算法、Lanczos 迭代、随机化算法）涉及极少。需要计算视角的读者必须转向 Golub--Van Loan 的 *Matrix Computations* 或 Trefethen--Bau 的 *Numerical Linear Algebra*。

**无穷维推广缺失**：本书严格限制在有限维矩阵的范围内，对 Hilbert 空间上的算子理论没有涉及。许多有限维结果在无穷维情形下需要本质性的修改甚至不再成立，而这些问题在泛函分析和量子力学中至关重要。对此感兴趣的读者需要参考 Reed--Simon 或 Conway 的算子理论教材。

**随机矩阵理论未涉及**：本书出版时，随机矩阵理论尚处于发展阶段。如今这一领域已在理论物理、数论和高维统计中占据核心位置，但本书对此没有讨论。

**概率和统计应用**：虽然本书的理论工具在统计学中广泛使用，但书中没有系统讨论矩阵分析在多元统计分析中的具体应用。这一空白部分由 Anderson 的 *An Introduction to Multivariate Statistical Analysis* 等专门教材填补。

**写作风格的门槛**：本书假设读者已具备扎实的线性代数基础。对于仅学过初等线性代数课程的学生，某些章节（特别是 Jordan 标准形和矩阵范数）可能存在较高的阅读门槛。

---

## 16. 延伸阅读

以下著作构成了围绕 Horn--Johnson 体系的核心参考文献网络：

1. **Horn, R. A. & Johnson, C. R.** *Topics in Matrix Analysis*. Cambridge University Press, 1991. 直接续篇，讨论数值域、稳定性、Hadamard 积等深层主题。

2. **Bhatia, R.** *Matrix Analysis*. Graduate Texts in Mathematics 169, Springer, 1997. 从算子理论视角深化矩阵分析，特别是扰动理论和优超理论。

3. **Gantmacher, F. R.** *The Theory of Matrices*, 2 volumes. Chelsea, 1959. 苏联学派的经典之作，提供互补的代数视角。

4. **Golub, G. H. & Van Loan, C. F.** *Matrix Computations*. Johns Hopkins University Press, 1983 (4th ed. 2013). 矩阵计算的标准参考，与 Horn--Johnson 构成理论/计算互补。

5. **Bellman, R.** *Introduction to Matrix Analysis*. McGraw-Hill, 1960; SIAM Classics, 2nd ed. 1997. 偏应用的矩阵分析经典，强调与动力系统和最优化的联系。

6. **Horn, R. A. & Garcia, S. R.** *Matrix Mathematics: A Second Course in Linear Algebra*. Cambridge University Press, 2nd ed. 2023. Horn 的最新教材，可作为 *Matrix Analysis* 的预备读物。

7. **Zhang, F.** *Matrix Theory: Basic Results and Techniques*. Springer, 2nd ed. 2011. 受 Horn--Johnson 影响的教材，对中国数学社区有重要影响。

8. **Marshall, A. W., Olkin, I. & Arnold, B. C.** *Inequalities: Theory of Majorization and Its Applications*. Springer, 2nd ed. 2011. 优超理论的权威参考，为矩阵不等式提供更广阔的数学背景。

---

## 17. 参考文献

- Horn, R. A. & Johnson, C. R. *Matrix Analysis*. Cambridge University Press, 1985. ISBN 0-521-30586-1. xiii + 561 pp.
- Horn, R. A. & Johnson, C. R. *Matrix Analysis*, 2nd edition. Cambridge University Press, 2013. ISBN 978-0-521-54823-6. xviii + 643 pp.
- Horn, R. A. & Johnson, C. R. *Topics in Matrix Analysis*. Cambridge University Press, 1991. ISBN 0-521-30587-X. viii + 607 pp.
- Bhatia, R. *Matrix Analysis*. Graduate Texts in Mathematics 169. Springer, 1997. ISBN 0-387-94846-5. xi + 349 pp.
- Gantmacher, F. R. *The Theory of Matrices*. 2 vols. Chelsea Publishing, 1959.
- Bellman, R. *Introduction to Matrix Analysis*. McGraw-Hill, 1960; 2nd ed. SIAM, 1997.
- Marcus, M. & Minc, H. *A Survey of Matrix Theory and Matrix Inequalities*. Allyn and Bacon, 1964. Reprinted by Dover, 1992.
- Golub, G. H. & Van Loan, C. F. *Matrix Computations*. Johns Hopkins University Press, 1983; 4th ed. 2013.
- Weyl, H. "Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen." *Mathematische Annalen*, 71(4): 441--479, 1912.
- Fan, K. "On a Theorem of Weyl Concerning Eigenvalues of Linear Transformations I." *Proceedings of the National Academy of Sciences*, 35(11): 652--655, 1949.
- Lidskii, B. V. "The proper values of the sum and the product of symmetric matrices." *Doklady Akademii Nauk SSSR*, 74: 769--772, 1950.
- Higham, N. J. "Second Edition (2013) of Matrix Analysis by Horn and Johnson." Blog post, January 28, 2013.
- *Linear Algebra and its Applications*, Volume 424, Issue 1, 2007. Special issue dedicated to Roger A. Horn.

---

*本文写作参考了 Cambridge University Press 出版信息、Semantic Scholar 引用数据、Google Scholar 作者档案以及 Nick Higham 的书评博客。*
