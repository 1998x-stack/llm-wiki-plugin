# Perron正矩阵定理：从连分数到谱理论的意外发现

## 作者

**Oskar Perron（奥斯卡·佩龙，1880--1975）**

德国数学家，生于弗兰肯塔尔（Frankenthal），卒于慕尼黑。1902年在慕尼黑大学获博士学位（导师为Ferdinand von Lindemann），此后曾赴哥廷根随David Hilbert研习。1906年于慕尼黑完成教授资格论文（Habilitation），1914至1922年任海德堡大学教授，1922至1951年任慕尼黑大学教授。Perron一生著述宏富，研究领域横跨连分数理论、微分方程、偏微分方程、数论与矩阵理论，其中以正矩阵特征值定理与求解Dirichlet问题的Perron方法最为后世所知。他撰写的连分数百科全书式专著《Die Lehre von den Kettenbruchen》至今仍是该领域的标准参考文献。

## 发表时间与出处

**1907年**，论文题为 *"Zur Theorie der Matrices"*（《论矩阵理论》），发表于 *Mathematische Annalen*，第64卷，第248--263页。同卷另有一篇密切相关的长文 *"Grundlagen fur eine Theorie des Jacobischen Kettenbruchalgorithmus"*（第11--76页），系统阐述了Jacobi连分数算法的基础理论，正是在后者的研究过程中，Perron发现了正矩阵的谱结构性质。

## 一句话概括

Perron证明了每个元素全为正数的方阵必然拥有一个唯一的最大正实特征值（Perron根），其对应的特征向量的所有分量均为正，且其余一切特征值的绝对值严格小于该Perron根——这一结果从连分数理论的技术性引理出发，最终开创了非负矩阵谱理论的全新领域。

---

## 一、历史背景与动机

十九世纪末至二十世纪初，连分数理论正处于蓬勃发展之中。普通一维连分数的收敛性理论已趋成熟，数学家们自然将目光投向更高维的推广——Jacobi连分数（多维连分数）。在慕尼黑大学，Alfred Pringsheim关于连分数的精彩讲座对青年Perron产生了深远影响，引导他将学术生涯的早期精力倾注于这一领域。

1907年，年仅27岁的Perron发表了他的教授资格论文的核心成果——一篇长达66页的论文《Grundlagen fur eine Theorie des Jacobischen Kettenbruchalgorithmus》，系统建立了Jacobi连分数算法的理论基础。在这篇宏文的第14节中，Perron考虑了一个特殊情形：当连分数的偏商（partial quotients）均为实数且非负时，收敛性分析归结为对一类具有正元素的矩阵的谱性质的研究。Perron陈述并证明了关于这类矩阵特征值分布的一个定理，他最初将其视为一个技术性辅助引理（Hilfsatz）——一个为了推导连分数收敛性所需的中间工具。

然而，Perron很快意识到这个"引理"本身蕴含着深刻的数学内涵，其意义远远超出了连分数的具体语境。他将这一结果从连分数理论中提炼出来，重新以矩阵理论的语言加以表述和证明，形成了独立的论文《Zur Theorie der Matrices》，发表于同一卷的《Mathematische Annalen》上。

这一学术历程堪称数学发现的经典范式：一个为特定问题服务的辅助工具，被敏锐的数学家识别为具有独立价值的基础性成果。Perron正矩阵定理的诞生，并非源于对矩阵理论的直接探索，而是连分数研究的一个意外而璀璨的副产品。

从更宏观的数学史视角来看，Perron的工作处于一个激动人心的时代交汇点。彼时，Hilbert正在哥廷根发展积分方程与算子理论，Frobenius在柏林推进有限群论与矩阵代数的系统研究，而概率论也在Markov等人手中经历着从古典向现代的深刻转型。Perron的定理恰好为这些看似不相关的领域提供了一个意想不到的桥梁。正如数学史家Thomas Hawkins所精辟指出的，非负矩阵理论"是一个在其起源和发展中完全由纯粹数学关切所驱动的理论，后来却被证明拥有极其广泛的应用谱系"。

## 二、核心问题

**正矩阵的特征值分布具有什么样的特殊结构？**

具体而言：给定一个 $n \times n$ 实方阵 $A = (a_{ij})$，其中所有元素 $a_{ij} > 0$，其特征多项式 $\det(A - \lambda I) = 0$ 的根（特征值）在复平面上如何分布？是否存在一个"主导"特征值？如果存在，它与其他特征值之间有怎样的量化关系？对应的特征向量有何特殊性质？

这些问题在Perron之前并未被系统地提出，更遑论解答。矩阵的特征值理论在当时主要关注对称矩阵（特征值全为实数）或正交矩阵等具有特殊代数结构的矩阵类。对于一般的非对称矩阵——特别是以元素正负性为出发点来刻画谱结构——这是一个全新的视角。

## 三、主要定理与结果

**定理（Perron，1907）。** 设 $A = (a_{ij})$ 为 $n \times n$ 实方阵，且所有元素满足 $a_{ij} > 0$（$1 \leq i, j \leq n$）。则：

**(i) 存在性与正性。** $A$ 存在一个正实特征值 $r > 0$，称为 **Perron根**（Perron root）或 **Perron--Frobenius特征值**。

**(ii) 主导性。** 对于 $A$ 的任何其他特征值 $\lambda$（可以是复数），均有
$$|\lambda| < r.$$
即Perron根严格大于所有其他特征值的绝对值，$r$ 等于 $A$ 的谱半径 $\rho(A)$。

**(iii) 单纯性。** $r$ 是 $A$ 的特征多项式的单根（simple root），即其代数重数为1。

**(iv) 正特征向量。** 对应于 $r$ 的特征向量可以选取为所有分量均为正的向量 $\mathbf{v} = (v_1, v_2, \ldots, v_n)^T$，$v_i > 0$ 对所有 $i$ 成立。进一步，$r$ 对应的特征空间是一维的（几何重数也为1），从而正特征向量在相差正常数倍的意义下是唯一的。

**(v) 唯一性。** $r$ 是 $A$ 的唯一具有正特征向量的特征值。

用现代线性代数的语言重新表述：正矩阵的谱半径本身是一个特征值，它是单纯的、正实的，且是唯一拥有（分量全正的）正特征向量的特征值；所有其他特征值都被严格地"困"在以原点为圆心、以Perron根为半径的开圆盘内部。

这一结果的优美之处在于，它仅从矩阵元素的正性这一初等条件出发，就得到了关于特征值分布的极其精确的全局性信息——而这些信息对于一般矩阵是完全不成立的。

## 四、核心方法与证明思路

Perron在1907年的论文中实际上给出了两个证明，二者都具有高度的技术巧妙性。

**第一个证明**基于对特征多项式的直接分析。Perron考察了正矩阵 $A$ 的特征多项式 $p(\lambda) = \det(\lambda I - A)$ 在正实轴上的行为。其核心思路可以概括如下：

1. **构造辅助函数。** 定义函数 $\varphi(\lambda)$ 为矩阵 $(\lambda I - A)^{-1}$ 的某种矩阵范数或迹。当 $\lambda$ 充分大时，$\lambda I - A$ 可逆且 $(\lambda I - A)^{-1}$ 的所有元素为正（可通过Neumann级数 $(\lambda I - A)^{-1} = \lambda^{-1}(I - \lambda^{-1}A)^{-1} = \lambda^{-1}\sum_{k=0}^{\infty} (\lambda^{-1}A)^k$ 看出）。

2. **分析奇异行为。** 当 $\lambda$ 从 $+\infty$ 沿正实轴减小时，$(\lambda I - A)^{-1}$ 的元素单调增大，直至在某个正实数 $r$ 处首次出现奇异（即 $\det(rI - A) = 0$）。这个 $r$ 就是 $A$ 的最大正实特征值。

3. **证明主导性。** 利用预解式（resolvent）$R(\lambda) = (\lambda I - A)^{-1}$ 在 $\lambda = r$ 处的极点性质，结合矩阵元素的正性，Perron论证了不可能存在模等于 $r$ 的其他特征值。

4. **证明正特征向量。** 通过分析 $R(\lambda)$ 在 $\lambda \to r^+$ 时的渐近行为，提取出对应于Perron根的特征向量，并利用矩阵元素的正性证明该特征向量的所有分量为正。

**第二个证明**更加代数化，直接利用了矩阵幂次 $A^k$ 的元素增长行为。

Perron的原始证明，特别是第一个证明，虽然技巧精湛，但其复杂性和所需的分析工具使得后来的数学家不断寻求更简洁、更透明的证明路径。在此后的近一百二十年间，Perron定理积累了大量风格各异的证明方法，至少包括以下几个主要流派：

- **Wielandt证明（1950）**：基于Frobenius的极大极小思想，利用正矩阵对正向量的"顺序保持"性质。这是目前大多数教科书采用的标准证明。

- **Brouwer不动点定理证明**：将正矩阵作用于单位单纯形（simplex）上的正向量集合，利用Brouwer不动点定理保证不动点的存在，从而获得Perron特征向量。

- **预解式证明（resolvent approach）**：这是最接近Perron原始思路的现代重述，被MacCluer（2000）称为"最自然的证明"，因为它"自然地流淌于围绕预解式理论的那个美丽的思想圈中"。

- **拓扑与序结构证明**：利用正锥（positive cone）上的Hilbert度量或Thompson度量，将Perron定理化归为压缩映射原理的推论。

每种证明方法都从不同角度揭示了Perron定理的数学本质，也反映了该定理与分析学、代数学、拓扑学多个分支的深刻联系。

## 五、重要性与地位

Perron 1907年的定理在数学史上的地位可以从以下几个层面来评估：

**开创性意义。** 它是非负矩阵理论（Nonnegative Matrix Theory）的奠基之作。在Perron之前，矩阵的谱理论主要关注具有特殊代数结构（对称性、正交性、酉性等）的矩阵类。Perron首次表明，矩阵元素的符号条件（正性）本身就足以决定谱结构的基本性质。这一视角的转变开辟了一个全新的研究方向。

**方法论革新。** Perron的工作展示了如何将"正性"作为一种结构性条件来利用——正矩阵将正向量映射为正向量，正锥在矩阵作用下保持不变。这种"正性方法"后来发展为泛函分析中正算子理论的核心思想，影响了Krein--Rutman定理（1948）等深刻推广。

**跨领域桥梁。** 该定理建立了纯代数对象（矩阵特征值）与"正性"这一具有鲜明物理/概率/经济直觉的性质之间的精确联系，使得矩阵理论能够系统地应用于概率论、经济学、人口学等以正量为基本变量的科学领域。

**持久的活力。** 自1907年至今，Perron定理（及其Frobenius推广）被持续地重新证明、推广和应用。MacCluer（2000）的综述记录了在近一个世纪间出现的多种证明方法，并指出"这个简单易懂的Perron结果，提供了一个无与伦比的载体，可以带领学生以一定深度游历众多应用领域"。

## 六、解决了什么瓶颈

在Perron的工作之前，数学家面对一般非对称矩阵的特征值问题时，缺乏有效的定性分析工具。一般矩阵的特征值可以是任意复数，可以有任意的代数与几何重数，其分布缺乏易于把握的规律性。

Perron定理解决了以下关键瓶颈：

**1. 主特征值的存在性与识别。** 对于一般矩阵，谱半径 $\rho(A)$ 虽然总是被某个特征值的模所达到，但该特征值可能不是实的、不是正的，也可能不是唯一的。Perron证明了对于正矩阵，谱半径不仅由一个正实特征值达到，而且该特征值是唯一的"最大"特征值。

**2. 特征向量的定性信息。** Perron在没有显式计算特征向量的情况下，证明了主特征向量的所有分量必须同号（可取为全正）。这一定性信息在应用中至关重要——例如，它保证了Markov链的平稳分布是一个真正的概率分布（所有分量非负）。

**3. 谱间隙的存在。** 主特征值与次特征值之间的严格分离（$|\lambda_2| < r$）意味着矩阵幂迭代的指数收敛性。这为后来的幂法（power method）提供了理论保障，也是Markov链遍历性的数学根基。

**4. 连分数收敛性的矩阵方法。** 在Perron的原始动机中，该定理为Jacobi连分数的收敛性分析提供了关键工具——多维连分数的逼近矩阵恰好具有正元素的性质，Perron根的存在性直接保证了连分数的收敛行为。

## 七、与前人工作的关系

Perron的工作并非凭空而来，它建立在十九世纪下半叶矩阵理论发展的丰厚基础之上。

**Frobenius的矩阵代数。** Georg Frobenius（1849--1917）在柏林建立了系统的矩阵代数理论，包括矩阵的秩理论、最小多项式、有理标准形等。Frobenius的工作为Perron提供了基本的概念框架和技术工具。值得注意的是，正是Perron 1907年的定理反过来激发了Frobenius在1908--1912年间对非负矩阵的系统研究。

**Hilbert的积分方程理论。** Perron曾在哥廷根随Hilbert学习。1904--1906年间，Hilbert发表了关于积分方程的系列论文，其中引入了算子谱的概念，并证明了对称核函数对应的积分算子具有实特征值和正交特征函数系。虽然Perron的正矩阵定理在技术层面并不直接依赖Hilbert的积分方程理论，但Hilbert关于谱理论的总体思想——特别是通过算子的结构性质来推断谱的定性信息——无疑对Perron产生了深刻的思想影响。

**Pringsheim的连分数理论。** Perron在慕尼黑的导师Alfred Pringsheim是连分数领域的重要人物。Pringsheim关于连分数收敛判据的一系列工作，直接引导Perron走向了Jacobi连分数的系统研究，从而间接催生了正矩阵定理。

**Sylvester与Cayley的矩阵理论。** 十九世纪中叶，Sylvester和Cayley创立了矩阵代数的基本语言。Sylvester关于特征方程（secular equation）的工作，以及Cayley--Hamilton定理（每个方阵满足其特征方程），都是Perron定理所依赖的背景知识。

## 八、后续影响与衍生

Perron 1907年的定理如同投入池塘的一颗石子，激起了持续一个多世纪的涟漪。

**Frobenius的推广（1908--1912）。** Perron定理发表仅一年后，Frobenius就开始了对其结果的深入研究和实质性推广。在1908和1909年的两篇短文《Uber Matrizen aus positiven Elementen》中，Frobenius给出了Perron定理的新证明，并引入了重要的极大极小刻画。1912年的长文《Uber Matrizen aus nicht negativen Elementen》是真正的里程碑：Frobenius将Perron的结果从正矩阵推广到了非负矩阵，引入了"不可约"（irreducible）与"本原"（primitive）的关键概念，并完整描述了不可约非负矩阵谱半径处的特征值分布——包括周期性现象。具体而言，Frobenius证明了：若 $A$ 是 $n \times n$ 不可约非负矩阵，其Perron根为 $r$，则在 $|\lambda| = r$ 的圆周上恰有 $h$ 个特征值（$h$ 为 $A$ 的周期），它们均匀分布为 $r e^{2\pi i k/h}$（$k = 0, 1, \ldots, h-1$）。这一精致的结果今日被称为 **Perron--Frobenius定理**。

**Markov链理论（1908--）。** 就在Perron定理发表后的第二年（1908年），A.A. Markov在完全不同的学术动机驱动下引入了Markov链的概念。Markov的目标是将大数定律和中心极限定理推广到相依随机变量的和，为此他研究了随机矩阵（转移矩阵）的幂次行为。尽管Markov并未引用Perron的工作，他在随机矩阵的特殊情形中独立地获得了Perron--Frobenius理论的若干关键结论。后来，正是von Mises首先明确建立了Markov链理论与Perron--Frobenius定理之间的形式化联系，Frechet和Romanovsky随后从这一视角系统发展了有限Markov链理论。

**泛函分析中的正算子理论。** Perron--Frobenius定理的无穷维推广是二十世纪泛函分析的重要篇章。1948年，M.G. Krein与M.A. Rutman证明了著名的Krein--Rutman定理：在具有正锥的Banach空间中，紧正算子的谱半径（若为正）是一个特征值，对应的特征向量属于正锥。这一定理可视为Perron定理在无穷维空间中的自然对应物，在偏微分方程（椭圆算子的主特征值）和数学物理中有深刻应用。

**动力系统与符号动力学。** 在遍历理论与符号动力学中，转移矩阵（transition matrix）的Perron--Frobenius特征值决定了子移位（subshift of finite type）的拓扑熵。Ruelle--Perron--Frobenius定理将这一思想推广到连续势函数的情形，成为热力学形式主义（thermodynamic formalism）的基石。

## 九、现代价值与应用

Perron定理及其推广在当代科学技术中的应用范围之广令人惊叹，以下列举最具影响力的几个方向。

**概率论与随机过程。** 有限状态Markov链的一切核心性质——平稳分布的存在性与唯一性、遍历性、混合速率——都可以从Perron--Frobenius定理优雅地推导出来。对于不可约、非周期的随机矩阵 $P$，Perron根恰为1，对应的左特征向量（归一化后）即为唯一的平稳分布 $\pi$；谱间隙 $1 - |\lambda_2|$ 则直接控制了收敛到平稳分布的速率。

**经济学：Leontief投入产出模型。** 1973年诺贝尔经济学奖得主Wassily Leontief的投入产出分析，其数学核心正是Perron--Frobenius定理。经济系统中 $n$ 个部门的相互依赖关系由一个非负消耗矩阵 $A$ 描述，Leontief矩阵 $(I - A)$ 可逆且逆矩阵非负（从而外部需求有正的生产解）的充要条件恰好是 $A$ 的Perron根 $\rho(A) < 1$。这就是著名的Hawkins--Simon条件的矩阵理论表述。Perron--Frobenius特征向量在经济均衡理论中也扮演着关键角色：它给出了在均衡增长路径上各部门产出的比例结构。

**Google PageRank算法。** 互联网搜索引擎的革命性核心——Google的PageRank算法——在本质上是Perron--Frobenius定理在超大规模稀疏矩阵上的计算应用。整个互联网的链接结构被建模为一个巨大的有向图，对应的邻接矩阵经过归一化和"阻尼因子"修正后，成为一个所有元素为正的列随机矩阵（Google矩阵）。Perron--Frobenius定理保证该矩阵存在唯一的Perron根1及其对应的正特征向量——这个特征向量的各分量就是网页的PageRank值。Larry Page和Sergey Brin在1998年的原始论文中使用阻尼因子 $\alpha = 0.85$，其数学作用恰恰是确保Google矩阵的所有元素为正（从而满足Perron定理的前提条件），同时保证幂迭代法以 $O(\alpha^k)$ 的速率收敛。据报道，对于早期的互联网规模，约50次迭代即可获得足够精确的PageRank向量。

**种群动力学：Leslie矩阵。** 在人口学与生态学中，种群的年龄结构动态由Leslie矩阵描述。Perron--Frobenius定理保证了在长期演化下，种群年龄分布趋近于一个稳定分布（Perron特征向量），而种群总量以Perron根为比率指数增长（或衰减）。这一结果对于渔业管理、濒危物种保护等实际决策具有直接指导意义。

**数值线性代数。** 幂法（power method）——最古老、最基本的特征值算法之一——其收敛性的理论保障正是Perron定理中的谱间隙条件。对于正矩阵（或更一般地，本原非负矩阵），迭代 $\mathbf{v}_{k+1} = A\mathbf{v}_k / \|A\mathbf{v}_k\|$ 从任意正初始向量出发都收敛到Perron特征向量，收敛速率由比值 $|\lambda_2|/r$ 决定。

**控制论与系统理论。** 在正系统（positive systems）理论中——即状态变量、输入和输出均取非负值的动态系统——Perron--Frobenius定理提供了稳定性分析的核心工具。系统矩阵的Perron根是否小于1，直接判定了离散时间正系统的渐近稳定性。

## 十、通俗化解释

想象一个拥有若干城市的国家，每天每个城市的居民都会按照固定的比例迁移到各个城市（包括留在原地）。如果这些比例都是正数——即每天确实有一部分人从任意一个城市搬到任意另一个城市——那么无论初始的人口分布是什么样的，经过足够长的时间后，人口分布都会趋近于一个固定的稳定比例。

Perron定理所说的"正特征向量"，就是这个长期稳定的人口分布；"Perron根"则描述了人口总量的长期增长（或衰减）趋势。而"其他特征值的绝对值严格小于Perron根"这一结论，保证了系统确实会收敛到这个稳定状态——初始条件的影响会以指数速率衰减，最终系统的行为完全由Perron根和Perron向量决定。

更形象地说：如果把矩阵反复作用于一个初始向量看作一台机器不断搅拌，那么Perron定理告诉我们，无论初始配料如何配比，这台机器最终都会搅拌出同样的"味道"（方向），只是"量"（大小）可能不同。

## 十一、阅读建议与路线图

对于希望深入理解Perron定理及其推广的读者，建议按照以下路线渐次推进：

**入门级（线性代数基础即可）：**
- Strang, G., *Linear Algebra and Its Applications*，第5章中关于正矩阵的讨论，提供了直观的几何解释。
- Meyer, C.D., *Matrix Analysis and Applied Linear Algebra*，第8章系统介绍了非负矩阵理论。

**中级（矩阵分析）：**
- Horn, R.A. & Johnson, C.R., *Matrix Analysis*（第2版，2013），第8章"Nonneg-ative Matrices"给出了Perron--Frobenius定理的完整证明与丰富应用。
- Seneta, E., *Non-negative Matrices and Markov Chains*（第2版，Springer，1981），从概率论视角出发，将Perron--Frobenius理论与Markov链理论融为一体。

**高级（泛函分析与算子理论）：**
- Bapat, R.B. & Raghavan, T.E.S., *Nonnegative Matrices and Applications*（Cambridge，1997），涵盖了组合学、博弈论等方向的高级应用。
- Schaefer, H.H., *Banach Lattices and Positive Operators*（Springer，1974），第一章从Banach格的视角给出了Perron--Frobenius理论的深刻推广。

**数学史：**
- Hawkins, T., "Continued fractions and the origins of the Perron--Frobenius theorem," *Archive for History of Exact Sciences* 62 (2008), 655--717。这是关于Perron定理起源的权威历史研究。
- MacCluer, C.R., "The many proofs and applications of Perron's theorem," *SIAM Review* 42 (2000), 487--498。综述了Perron定理的多种证明方法及其向各应用领域的传播。

## 十二、局限性与未解决问题

尽管Perron定理的核心结论清晰而完美，它在数学实践中面临着若干重要的局限和仍在活跃研究中的开放问题。

**1. 正性假设的限制。** Perron定理要求矩阵的所有元素严格为正。在实际应用中，许多自然出现的矩阵是非负的但含有零元素（如稀疏的转移矩阵）。虽然Frobenius 1912年的推广覆盖了不可约非负矩阵的情形，对于可约非负矩阵——特别是在大规模网络分析中频繁出现的情形——谱结构的完整刻画仍然是活跃的研究领域。

**2. 定量估计。** Perron定理是定性的：它断言谱间隙 $r - |\lambda_2|$ 严格为正，但并不给出其大小的定量下界。在应用中（如Markov链的混合时间估计、PageRank的收敛速率分析），谱间隙的定量估计至关重要。虽然已有大量关于谱间隙的研究成果（如Cheeger不等式及其离散类比），对一般正矩阵的最优谱间隙估计仍是一个困难问题。

**3. 无穷维推广的复杂性。** Krein--Rutman定理虽然将Perron定理推广到了Banach空间中的紧正算子，但对于非紧算子（如某些偏微分方程的解算子），类似的谱结论可能不成立，或者需要更精细的条件。正算子谱理论在无穷维空间中的完整图景仍未完全厘清。

**4. 计算复杂性。** 对于 $n$ 很大的正矩阵，精确计算Perron根和Perron向量在计算上是困难的。幂法虽然概念简单，但收敛速率取决于谱间隙的大小；当 $|\lambda_2|/r$ 接近1时，收敛可能极其缓慢。高效的Perron根计算算法（如基于Krylov子空间方法的变体）仍然是数值线性代数的重要研究方向。

**5. 非线性推广。** 近年来，将Perron--Frobenius理论推广到非线性映射（如张量特征值问题、非负张量的谱理论）和非交换情形（如矩阵联合谱半径）已成为活跃的研究前沿。这些推广在量子信息论、信号处理等新兴领域有着潜在的重要应用。

## 十三、相关重要后续论文

1. **Frobenius, G.** (1908). "Uber Matrizen aus positiven Elementen," *Sitzungsberichte der Koniglich Preussischen Akademie der Wissenschaften zu Berlin*, 471--476. Frobenius对Perron定理的首次回应，给出了新证明并引入了极大极小刻画。

2. **Frobenius, G.** (1912). "Uber Matrizen aus nicht negativen Elementen," *Sitzungsberichte der Koniglich Preussischen Akademie der Wissenschaften zu Berlin*, 456--477. 将Perron定理推广到不可约非负矩阵，引入不可约性和周期性概念，完成了今日所称"Perron--Frobenius定理"的全部内容。

3. **Markov, A.A.** (1908). "Rasprostranenie zakona bol'shikh chisel na velichiny, zavisyashchie drug ot druga," *Izvestiya Fiziko-Matematicheskogo Obshchestva pri Kazanskom Universitete*, 2-ya seriya, tom 15, 135--156. Markov链理论的奠基性论文，在随机矩阵的特殊情形中独立触及了Perron--Frobenius理论的核心内容。

4. **Wielandt, H.** (1950). "Unzerlegbare, nicht negative Matrizen," *Mathematische Zeitschrift*, 52, 642--648. 给出了Perron--Frobenius定理至今最简洁优雅的证明之一，成为标准教科书采用的版本。

5. **Krein, M.G. & Rutman, M.A.** (1948). "Lineynye operatory, ostavlyayushchie invariantnoy konus v prostranstve Banakha," *Uspekhi Matematicheskikh Nauk*, 3(1), 3--95. 英文翻译: "Linear operators leaving invariant a cone in a Banach space," *AMS Translations*, Ser. 1, 10, 199--325 (1962). 将Perron--Frobenius定理推广到无穷维Banach空间中的紧正算子。

6. **Brin, S. & Page, L.** (1998). "The anatomy of a large-scale hypertextual web search engine," *Computer Networks and ISDN Systems*, 30, 107--117. Google搜索引擎的奠基论文，PageRank算法的实质正是Perron--Frobenius定理在超大规模稀疏正矩阵上的计算实现。

7. **MacCluer, C.R.** (2000). "The many proofs and applications of Perron's theorem," *SIAM Review*, 42(3), 487--498. 系统综述了Perron定理自1907年以来的多种证明方法及其跨学科传播。

8. **Hawkins, T.** (2008). "Continued fractions and the origins of the Perron--Frobenius theorem," *Archive for History of Exact Sciences*, 62, 655--717. 关于Perron--Frobenius定理起源的权威数学史研究。

## 十四、进一步阅读

**原始文献：**
- Perron, O. (1907). "Zur Theorie der Matrices," *Mathematische Annalen*, 64, 248--263. 可通过Springer数字化档案获取：[DOI: 10.1007/BF01449896](https://link.springer.com/article/10.1007/BF01449896)
- Perron, O. (1907). "Grundlagen fur eine Theorie des Jacobischen Kettenbruchalgorithmus," *Mathematische Annalen*, 64, 11--76.

**现代教科书：**
- Horn, R.A. & Johnson, C.R., *Matrix Analysis*（第2版），Cambridge University Press, 2013.
- Seneta, E., *Non-negative Matrices and Markov Chains*（第2版），Springer, 1981.
- Berman, A. & Plemmons, R.J., *Nonnegative Matrices in the Mathematical Sciences*, SIAM Classics, 1994.
- Minc, H., *Nonnegative Matrices*, Wiley, 1988.
- Varga, R.S., *Matrix Iterative Analysis*（修订扩充第2版），Springer, 2000.

**综述与历史：**
- MacCluer, C.R. (2000). ["The many proofs and applications of Perron's theorem,"](https://epubs.siam.org/doi/10.1137/S0036144599359449) *SIAM Review*, 42(3), 487--498.
- Hawkins, T. (2008). ["Continued fractions and the origins of the Perron--Frobenius theorem,"](https://link.springer.com/article/10.1007/s00407-008-0026-x) *Archive for History of Exact Sciences*, 62, 655--717.
- Seneta, E. (2006). ["Markov and the creation of Markov chains,"](https://www.maths.usyd.edu.au/u/eseneta/senetamcfinal.pdf) in *MAM 2006: Markov Anniversary Meeting*, Boson Books, 1--20.

**在线资源：**
- [Perron--Frobenius theorem -- Wikipedia](https://en.wikipedia.org/wiki/Perron%E2%80%93Frobenius_theorem)
- [Oskar Perron -- MacTutor History of Mathematics](https://mathshistory.st-andrews.ac.uk/Biographies/Perron/)
- [Nick Higham: What Is the Perron--Frobenius Theorem?](https://nhigham.com/2021/07/13/what-is-the-perron-frobenius-theorem/)
- [QuantEcon: The Perron-Frobenius Theorem (with Python)](https://intro.quantecon.org/eigen_II.html)

---

*本文写作参考了Perron原始论文、Hawkins的历史研究、MacCluer的综述论文以及上述教科书。文中所有数学陈述均基于标准文献，力求在学术严谨性与可读性之间取得平衡。*
