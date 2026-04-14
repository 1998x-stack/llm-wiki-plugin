# 加藤敏夫《线性算子的扰动理论》（1966）：从矩阵到算子的扰动分析统一

---

## 1. 标题

**Perturbation Theory for Linear Operators**
（线性算子的扰动理论）

---

## 2. 作者

**Tosio Kato**（加藤敏夫，1917年8月25日 -- 1999年10月2日）

加藤敏夫出生于日本栃木县�的鹿沼市，是二十世纪最杰出的数学物理学家之一。他在东京帝国大学攻读理论物理，1941年获得本科学位。第二次世界大战期间，加藤因患肺结核而被迫中断学术活动，但正是在这段被迫隔绝的岁月里，他独立完成了算子自伴性和扰动理论的核心工作——后来他在 Norbert Wiener 奖的获奖致辞中提到，这些结果"在战争结束前就已基本完成"。1951年他在东京大学获得博士学位，同年发表了证明原子与分子 Schrodinger Hamilton 算子本质自伴性的里程碑论文。1958年成为东京大学教授，1962年转赴加州大学伯克利分校担任数学教授直至退休。他一生发表了超过160篇论文和6部专著，研究领域横跨算子理论、量子力学、流体力学和偏微分方程。1980年，他因在扰动理论和偏微分方程方面的杰出贡献而获得美国数学会与工业与应用数学会联合颁发的 Norbert Wiener 应用数学奖。1970年，他在尼斯举行的国际数学家大会上作了题为"Scattering Theory and Perturbation of Continuous Spectra"的大会报告。

---

## 3. 发表时间与刊物

- **首版**：1966年，Springer-Verlag（Berlin / Heidelberg / New York）
- **丛书**：Grundlehren der mathematischen Wissenschaften（数学科学基础丛书），Band 132
- **页数**：xix + 592页
- **第二版**：1976年，增加了补充注释和补充参考文献，对若干段落进行了重写
- **经典重印**：1995年、2011年、2014年由 Springer 以"Classics in Mathematics"系列重新出版
- **简明版**：加藤另著有 *A Short Introduction to Perturbation Theory for Linear Operators*，将前两章独立成册面向更广泛的读者

---

## 4. 一句话概括

本书建立了线性算子扰动理论的完整数学框架，统一了有限维矩阵与无穷维算子的谱扰动分析，为量子力学、数值分析和现代泛函分析提供了坚实的理论基石。

---

## 5. 历史背景

二十世纪上半叶，量子力学的发展向数学家提出了一系列深刻的挑战。量子力学的数学语言是 Hilbert 空间中的算子理论：可观测量对应自伴算子，能量本征值对应算子的谱。然而，物理上真实存在的 Hamilton 算子——如包含 Coulomb 奇异势能的原子和分子 Hamilton 量——其数学性质远非平凡。甚至 von Neumann 这位算子理论的奠基人也未能证明这些算子的自伴性。

扰动理论的思想可以追溯至更早。1897年，Lord Rayleigh 在研究声波问题时提出了扰动展开的物理方法。1926年，Schrodinger 在创立量子力学的系列论文中系统地使用了扰动级数来计算原子能级。然而，这些方法缺乏严格的数学基础。

Franz Rellich 在1937至1942年间发表了五篇开创性的系列论文，首次为扰动理论建立了严格的数学框架。他证明了自伴矩阵族的实解析特征值定理：如果 Hermite 矩阵 $A(t)$ 的矩阵元素是参数 $t$ 的实解析函数，那么其特征值和特征向量也可以选取为 $t$ 的实解析函数。Rellich 的证明基于 Puiseux 定理，将代数函数论的工具引入算子扰动。但 Rellich 也意识到，这种解析依赖性在多参数情形下会崩溃——他给出了一个简单的 $2 \times 2$ 矩阵反例，其特征值 $\pm\sqrt{\beta^2 + \gamma^2}$ 在原点处不可微。

与此同时，von Neumann 和 Stone 建立了无穷维 Hilbert 空间中自伴算子的谱理论基础。1935年，von Neumann 证明了一个深刻的结果：任何自伴算子都可以通过任意小的 Hilbert-Schmidt 紧算子扰动变为纯点谱算子，这就是著名的 Weyl-von Neumann 定理。该定理表明，本质谱是自伴算子在紧扰动下唯一稳定的谱特征。

加藤的学术生涯始于这一大背景之下。在战争期间的隔绝中，他独立地重新发现了 Rellich 和 Sz.-Nagy 的许多结果，同时开创了渐近扰动理论——这是 Rellich 未曾涉及的领域。1947年，Sz.-Nagy 在两篇论文中将 Rellich 的工作扩展到 Hilbert 空间的自伴算子情形和 Banach 空间的一般闭算子情形，引入了谱投影的围道积分表示。加藤后来也独立发展了这些工具。1951年，加藤发表了他最具影响力的单篇论文"Fundamental Properties of Hamiltonian Operators of Schrodinger Type"，证明了所有由有限个 Coulomb 相互作用粒子组成的量子系统的 Hamilton 算子在 $L^2(\mathbb{R}^{3N})$ 上本质自伴。这一结果的证明方法——后来被称为 Kato-Rellich 定理——简洁而有力：如果 $A$ 是自伴算子，$B$ 是 $A$-有界的且相对界小于1，则 $A + B$ 自伴。这为量子力学的全部理论计算提供了数学合法性。

到1960年代初，泛函分析已经成熟为一门系统的学科。半群理论（由 Hille 和 Yosida 发展）、谱理论、Banach 代数、算子代数等分支已经形成完整的体系。加藤在伯克利的位置使他能够综合这些发展，将分散在数十年物理文献和数学论文中的扰动理论结果统一为一部体系化的专著。

---

## 6. 核心问题

本书所解决的核心数学问题可以精确表述如下：

设 $T(\kappa)$ 是依赖于参数 $\kappa$ 的线性算子族，当 $\kappa = 0$ 时 $T(0) = T$ 是一个已知的算子（其谱性质完全清楚）。问题是：当 $\kappa$ 偏离零时，即算子 $T$ 受到扰动 $T(\kappa) = T + \kappa T^{(1)} + \kappa^2 T^{(2)} + \cdots$ 时，$T(\kappa)$ 的谱（特征值、特征空间、本质谱、连续谱）如何依赖于参数 $\kappa$？这种依赖是连续的、解析的，还是可能出现突变？

具体而言，需要回答以下子问题：（1）特征值是否作为 $\kappa$ 的连续或解析函数而变化？（2）特征空间（不变子空间）在扰动下如何旋转？（3）本质谱在何种扰动下保持稳定？（4）当正则扰动条件不满足时（奇异扰动），特征值的渐近行为如何？（5）散射理论中的波算子何时存在且完备？

---

## 7. 主要定理与结果

本书包含十章，系统地建立了以下核心结果：

**（一）谱连续性定理**。对于 Banach 空间中的有界算子族，如果算子范数连续依赖于参数，则谱作为集合是上半连续的。对于紧算子族，离散特征值是连续函数。

**（二）解析扰动理论（Kato-Rellich 定理）**。对于自伴算子 $A$ 和对称算子 $B$，若 $B$ 是 $A$-有界的且相对界 $a < 1$，即存在常数 $a, b$ 使得 $\|Bu\| \leq a\|Au\| + b\|u\|$ 对所有 $u \in D(A)$ 成立，则 $A + B$ 在 $D(A)$ 上自伴。由此推出，$T(\kappa) = A + \kappa B$ 的离散特征值可以展开为 $\kappa$ 的收敛幂级数。

**（三）渐近扰动理论**。当解析扰动条件不满足时——例如扰动改变了算子的定义域（奇异扰动）——加藤发展了特征值的渐近展开理论，给出了 Puiseux 级数形式的分支行为分析。

**（四）半有界形式扰动**。利用二次型（sesquilinear form）方法，加藤处理了比算子有界扰动更广泛的情形，建立了 KLMN 定理（Kato-Lax-Milgram-Nelson），使得某些奇异势能（如量子力学中的 $1/r^2$ 势）也能纳入理论框架。

**（五）Weyl-von Neumann 定理的推广**。本质谱在相对紧扰动下保持不变：$\sigma_{\text{ess}}(T) = \sigma_{\text{ess}}(T + K)$。本书给出了系统的证明并讨论了各种推广形式。

**（六）子空间之间的间距（Gap）**。加藤引入了 Hilbert 空间中子空间对理论，定义了两个闭子空间之间的"间距"度量，并证明了当间距小于1时两个投影通过酉变换相联系。

**（七）散射理论基础**。第十章发展了波算子的存在性和完备性理论，证明了迹类扰动下波算子 $\Omega^{\pm}(H, H_0)$ 的存在性和完备性（Kato-Birman 定理），并引入了"Kato 光滑性"概念作为证明波算子存在性的关键工具。

---

## 8. 核心方法

加藤在本书中综合运用了多种深刻的数学方法：

**围道积分与谱投影**。继承 Sz.-Nagy 的思想，加藤将 Cauchy 积分公式推广到算子族：谱投影 $P(\kappa) = -\frac{1}{2\pi i} \oint_\Gamma (T(\kappa) - z)^{-1} dz$ 是参数 $\kappa$ 的解析函数。通过选取围绕目标特征值的适当围道 $\Gamma$，可以从预解式的解析性推导出特征值和特征空间的解析依赖性。

**算子半群理论**。第九章系统地发展了 Banach 空间中强连续算子半群（$C_0$-半群）的理论，包括 Hille-Yosida 生成定理和 Trotter-Kato 逼近定理。这为抛物型和双曲型偏微分方程的扰动分析提供了框架。

**二次型方法（Sesquilinear Forms）**。第六章深入讨论了 Hilbert 空间中的半有界二次型，通过 Friedrichs 扩张将二次型与自伴算子联系起来。这使得扰动理论能够处理定义域不同的算子之扰动——一个纯粹从算子有界扰动角度无法触及的领域。

**子空间对理论**。加藤发展了两个闭子空间之间"间距"的系统理论，定义 $\delta(M, N) = \sup_{u \in M, \|u\|=1} \text{dist}(u, N)$，并建立了间距与投影差之范数之间的精确关系。这一工具在后来的数值分析和统计学中得到了广泛应用。

**Kato 光滑性**。加藤定义了算子 $G$ 相对于自伴算子 $H$ 的"光滑性"条件：$\int_{-\infty}^{\infty} \|G e^{-iHt} f\|^2 dt \leq C \|f\|^2$。这一条件比迹类条件更容易在具体问题中验证，成为散射理论中证明波算子存在性的核心工具。

---

## 9. 重要性与影响

加藤的这部专著是二十世纪数学中被引用次数最多的著作之一，截至目前累计被引用超过21000次。它的影响力横跨纯数学、应用数学、理论物理和计算科学等多个领域。

在数学方面，本书首次将有限维矩阵扰动（以 Wilkinson 的数值分析传统为代表）和无穷维算子扰动（以 Rellich-Sz.-Nagy 的泛函分析传统为代表）统一在同一个概念框架内。书中前两章处理有限维空间中的算子理论和扰动理论，后续章节自然地过渡到 Banach 空间和 Hilbert 空间。这种"从有限维到无穷维"的逻辑架构使得矩阵论专家和泛函分析专家能够在同一部著作中找到各自需要的结果，同时看到两个领域之间的深层联系。

在物理学方面，本书为量子力学中的扰动计算提供了完整的数学正当性。从 Rayleigh-Schrodinger 扰动级数的收敛性，到散射矩阵的数学基础，再到量子场论中重整化群方法的算子理论背景，加藤的框架无处不在。Barry Simon 在其四卷本巨著 *Methods of Modern Mathematical Physics*（与 Reed 合著）中大量引用和发展了加藤的理论，使其成为现代数学物理教育的核心组成部分。

在数值计算方面，Kato-Rellich 理论中的误差估计和扰动界为数值线性代数中的稳定性分析提供了理论依据。Wilkinson 的矩阵计算误差理论和加藤的算子扰动理论在本书中实现了概念上的对接，为后来的数值分析发展奠定了基础。

---

## 10. 解决了什么瓶颈

在本书出版之前，扰动理论存在几个严重的碎片化问题：

**矩阵扰动与算子扰动的分离**。矩阵特征值的扰动分析（源于 Weyl 1912年的不等式和后来 Wilkinson 的工作）和无穷维算子的谱扰动分析（源于 Rellich、Sz.-Nagy 的工作）是两个几乎独立发展的领域，使用不同的语言和工具，研究者之间交流甚少。加藤在书序中明确指出，直到1966年本书出版，Rellich 和 Sz.-Nagy 的结果"并未广为人知"。

**缺乏系统化的参考文献**。扰动理论的结果散布在数十年间数百篇论文中——从 Rayleigh 的物理直觉，到 Rellich 的德文论文，到 Sz.-Nagy 的匈牙利文论文，到各个应用领域的特殊结果。研究者缺乏一部能够提供全景视野的综合参考书。

**正则扰动与奇异扰动的混淆**。在加藤之前，何时扰动是"正则的"（特征值可以展开为收敛幂级数），何时是"奇异的"（需要分数幂或渐近展开），并没有清晰的判别标准。加藤给出了系统的分类框架。

**散射理论缺乏算子理论基础**。量子力学的散射理论虽然在物理上已经十分成熟，但其数学基础——特别是波算子的存在性和完备性——缺乏严格的证明。加藤的迹类扰动理论和光滑性方法填补了这一空白。

---

## 11. 与前人工作的关系

**Rellich 的解析扰动理论（1937-1942）**。Rellich 是严格扰动理论的开创者，他在五篇系列论文中详尽处理了有限维情形，并开始涉及自伴算子的无穷维推广。加藤在书中系统地整合并推广了 Rellich 的全部结果，特别是在渐近扰动和非自伴算子情形做了本质性的扩展。Kato-Rellich 定理——自伴性在相对有界扰动下的稳定性——虽然以二人命名，但其在一般 N 体量子系统中的应用是加藤的独创贡献。

**Sz.-Nagy 的贡献（1947, 1951）**。Sz.-Nagy 将 Rellich 的工作从有限维推广到 Hilbert 空间，引入了谱投影的围道积分方法，证明了当两个正交投影之差的范数小于1时，它们通过酉变换相联系。加藤吸收了这些工具并进一步发展了子空间对理论。此外，Sz.-Nagy 的酉膨胀定理为算子扰动理论中的酉等价问题提供了重要工具。

**Weyl-von Neumann 定理**。Weyl（1910）首先定义了本质谱的概念并证明其在紧扰动下的稳定性。von Neumann（1935）证明了逆命题：两个具有相同本质谱的自伴算子，模紧算子酉等价。加藤在书中将这些结果置于统一框架下，并推广到相对紧扰动的情形。

**Wilkinson 的数值矩阵扰动（1965）**。J.H. Wilkinson 的 *The Algebraic Eigenvalue Problem*（1965）几乎与加藤的书同时出版，但从数值计算的角度处理矩阵特征值问题。加藤的前两章涵盖了 Wilkinson 方法的理论内核，同时提供了通向无穷维推广的桥梁。

**Friedrichs 的形式扩张**。K.O. Friedrichs 发展的半有界算子的二次型方法被加藤纳入第六章，成为处理奇异势能扰动的核心工具。

---

## 12. 对后续工作的影响

**Davis-Kahan sin theta 定理（1970）**。Chandler Davis 和 William Kahan 在1970年发表的关于特征向量扰动的经典论文，直接建立在加藤的子空间间距理论之上。该定理给出了两个矩阵的不变子空间之间的主角正弦与扰动范数及谱间隙之间的定量关系：$\|\sin \Theta\| \leq \|H\| / \delta$，其中 $\delta$ 是谱间隙。这一结果在现代统计学和机器学习中得到了爆发性的应用——它是分析主成分分析（PCA）一致性、谱聚类稳定性和社区发现算法的核心数学工具。

**Reed-Simon《现代数学物理方法》（1972-1978）**。Barry Simon 和 Michael Reed 的四卷本巨著是现代数学物理的标准教材，其中大量采用了加藤的框架。第二卷 *Fourier Analysis, Self-Adjointness* 系统地使用了 Kato-Rellich 定理；第三卷 *Scattering Theory* 的核心是 Kato-Birman 方法；第四卷 *Analysis of Operators* 发展了 Kato 光滑算子理论。可以说，Reed-Simon 是加藤思想在数学物理教育中的最重要传播渠道。

**Bhatia 的矩阵分析（1987, 1997）**。Rajendra Bhatia 的著作 *Perturbation Bounds for Matrix Eigenvalues*（1987）和 *Matrix Analysis*（1997）继承了加藤在矩阵扰动方面的传统，发展了谱变分不等式的系统理论。Bhatia 与 Davis 在1984年关于酉矩阵特征值扰动的合作，直接源于加藤书中建立的理论框架。

**量子力学散射理论的完备化**。加藤在第十章建立的波算子理论被后续研究者大幅推进。Deift 和 Simon 受加藤思想启发，证明了多通道散射的完备性等价于特定波算子的存在性。Enss 方法、Mourre 估计等现代散射理论工具都可以追溯到加藤的光滑性理论。

**偏微分方程的半群方法**。第九章的半群理论对后续的偏微分方程研究产生了深远影响。Trotter-Kato 逼近定理成为数值偏微分方程和随机分析中的基本工具，加藤本人后来也在 Navier-Stokes 方程和 KdV 方程的数学理论中做出了重要贡献（"Kato 光滑效应"，1983）。

---

## 13. 现代价值

半个多世纪后的今天，加藤的扰动理论框架在多个前沿领域焕发着新的生命力：

**量子计算中的误差分析**。量子计算的核心挑战之一是退相干和门操作误差对计算结果的影响。这本质上是一个算子扰动问题：量子门对应酉算子，噪声对应对这些酉算子的扰动。加藤建立的谱扰动界为量子纠错码的设计和量子算法的容错性分析提供了理论工具。近年来，研究者们已经开始在量子计算机上直接实现扰动理论计算——利用量子信号处理（Quantum Signal Processing）技术来高效计算扰动能量。

**谱聚类与图 Laplacian 扰动**。在机器学习和数据科学中，谱聚类算法通过分析数据相似性矩阵（图 Laplacian）的特征向量来发现数据的内在结构。当数据受到噪声污染时，图 Laplacian 被扰动，其特征向量也随之变化。Davis-Kahan sin theta 定理——直接源于加藤的子空间理论——是分析这种变化的标准工具，已成为理论机器学习文献中引用最频繁的经典结果之一。

**随机矩阵理论**。在分析高维统计模型时，样本协方差矩阵可以视为总体协方差矩阵的扰动。加藤理论中的谱连续性和特征空间稳定性结果为理解 Marchenko-Pastur 律、Tracy-Widom 分布等随机矩阵极限定理提供了确定性的骨架。

**凝聚态物理中的拓扑相**。拓扑绝缘体和拓扑超导体的分类依赖于 Hamilton 量在绝热扰动下的谱间隙稳定性。加藤在1950年独立证明的量子绝热定理，以及本书中建立的解析扰动理论，为理解拓扑保护态的稳定性提供了数学基础。

**数值线性代数**。现代大规模特征值计算（如 Lanczos 算法、隐式重启 Arnoldi 方法）的收敛性和稳定性分析，本质上依赖于加藤书中建立的谱扰动框架。

---

## 14. 通俗解读

想象一个由许多弹簧和质量块组成的振动系统。每个质量块的固有振动频率取决于弹簧的刚度和质量块的大小——这些频率就是系统的"特征值"。现在，如果我们稍微调整某根弹簧的刚度，或者在某个质量块上添加一小块额外的质量，整个系统的振动频率会怎样变化？

这就是扰动理论要回答的核心问题。在有限个弹簧的情形，答案相对直观：小的调整导致频率的小变化，而且这种变化是光滑的、可预测的——你可以用泰勒级数来计算新的频率。

但量子力学面对的是"无穷多根弹簧"的情形——一个电子在原子核的库仑势场中运动，其能级由一个无穷维空间中的算子决定。在这种情形下，"小扰动导致小变化"这一直觉不再理所当然。可能出现的病态行为包括：特征值突然消失、从连续谱中分裂出离散能级、特征空间发生剧烈旋转、甚至算子本身失去数学意义（不再自伴）。

加藤的伟大贡献在于：他精确地刻画了"什么情况下直觉是对的"——在满足特定条件（如相对有界性）时，无穷维算子的谱确实像有限维矩阵一样表现良好；他同时精确地描述了"直觉失效时会发生什么"——在奇异扰动的情形下，特征值以分数幂次分裂，需要全新的渐近分析工具。

---

## 15. 阅读指南

由于本书结构严谨、逻辑层次分明，不同背景的读者可以选择不同的阅读路径：

**数值线性代数与矩阵分析方向**：第一章（有限维算子理论）和第二章（有限维扰动理论）构成了一个自包含的整体，已被加藤单独出版为 *A Short Introduction to Perturbation Theory for Linear Operators*。这两章即使不具备泛函分析背景的读者也可以阅读，适合矩阵计算和数据科学领域的研究者。

**泛函分析与算子理论方向**：在完成前两章后，按序阅读第三章（Banach 空间算子引论）、第四章（Banach 空间中的稳定性与扰动理论）、第五章（Hilbert 空间算子）。这些章节构成了从有限维到无穷维的自然过渡。

**量子力学与数学物理方向**：重点是第五章（Hilbert 空间算子）、第六章（半线性形式理论，含 Kato-Rellich 定理的完整证明）、第七章（解析扰动理论）和第十章（散射理论）。建议同时参考 Reed-Simon 的相关卷次以获得更多物理动机。

**偏微分方程方向**：第九章（半群理论）是核心，但需要第三至五章作为铺垫。

**通读建议**：第八章（渐近扰动理论）是技术上最困难的部分之一，初次阅读可以跳过细节，重点理解正则扰动与奇异扰动的区分标准。

---

## 16. 局限性

尽管本书是扰动理论的经典之作，但对现代读者而言也存在一些局限：

**高度抽象**。本书以最一般的形式——Banach 空间中的闭算子——来陈述大多数结果，这对于只需要有限维矩阵扰动界的应用者（如统计学家或机器学习研究者）来说门槛过高。Davis-Kahan sin theta 定理在原书中以非常抽象的形式出现，而大多数应用者实际需要的是其有限维特化版本。

**计算方面的薄弱**。本书侧重理论框架的建立，对于如何在具体问题中获得最优的定量估计着墨不多。例如，扰动级数的收敛半径的具体计算、特征值扰动界的锐化等问题，需要参考后续的专门文献。

**时代局限**。第二版（1976年）之后再未更新。1980年代以来的重要发展——如 Mourre 估计、半经典分析、非自伴算子的伪谱理论、随机算子谱理论等——均未被纳入。书中对数值算法和计算实践的讨论也反映了1960年代的计算水平。

**散射理论的不完整性**。第十章虽然开创性地将散射理论纳入了扰动理论框架，但由于该领域在1970-90年代经历了爆发式发展（N 体渐近完备性、Enss 方法等），书中的处理已显得过于初步。

**符号与记法的时代性**。某些符号约定（如用 $T$ 而非 $H$ 表示 Hamilton 算子，用 $\kappa$ 而非 $\lambda$ 表示扰动参数）与当代数学物理文献不完全一致，可能给初学者带来对照困难。

---

## 17. 延伸阅读

1. **Reed, M. & Simon, B.** *Methods of Modern Mathematical Physics*, Vol. I--IV, Academic Press, 1972--1978. 现代数学物理的标准教材，系统发展了加藤的许多思想。

2. **Bhatia, R.** *Perturbation Bounds for Matrix Eigenvalues*, SIAM Classics in Applied Mathematics, 2007 (expanded edition). 矩阵特征值扰动界的专门著作，包含加藤理论的有限维特化。

3. **Bhatia, R.** *Matrix Analysis*, Graduate Texts in Mathematics 169, Springer, 1997. 矩阵分析的经典教材，包含谱变分理论和算子不等式。

4. **Simon, B.** "Tosio Kato's work on non-relativistic quantum mechanics," *Bulletin of Mathematical Sciences*, 8(1), 121--232, 2018. Barry Simon 对加藤在量子力学方面全部工作的权威综述。

5. **Chatelin, F.** *Spectral Approximation of Linear Operators*, Academic Press, 1983. 从数值分析角度讨论算子谱的逼近与扰动。

6. **Stewart, G.W. & Sun, J.** *Matrix Perturbation Theory*, Academic Press, 1990. 矩阵扰动理论的系统教材，衔接了加藤的理论框架与计算实践。

7. **Yafaev, D.R.** *Mathematical Scattering Theory: Analytic Theory*, AMS Mathematical Surveys and Monographs, Vol. 158, 2010. 散射理论的现代权威参考书，全面发展了加藤-Birman 方法。

8. **Rellich, F.** *Perturbation Theory of Eigenvalue Problems*, Gordon and Breach, 1969. Rellich 自己的讲义集，是加藤工作的直接前驱。

---

## 18. 参考文献

1. Kato, T. *Perturbation Theory for Linear Operators*. Grundlehren der mathematischen Wissenschaften, Band 132. Springer-Verlag, Berlin-Heidelberg-New York, 1966. xix + 592 pp. (Second edition, 1976; reprinted as Classics in Mathematics, 1995.)

2. Kato, T. "Fundamental Properties of Hamiltonian Operators of Schrodinger Type." *Transactions of the American Mathematical Society*, 70(2): 195--211, 1951.

3. Rellich, F. "Storungstheorie der Spektralzerlegung, I--V." *Mathematische Annalen*, 113: 600--619, 1937; 113: 677--685, 1937; 116: 555--570, 1939; 117: 356--382, 1940; 118: 462--484, 1942.

4. Sz.-Nagy, B. "Perturbations des transformations autoadjointes dans l'espace de Hilbert." *Commentarii Mathematici Helvetici*, 19: 347--366, 1947.

5. Davis, C. & Kahan, W.M. "The Rotation of Eigenvectors by a Perturbation. III." *SIAM Journal on Numerical Analysis*, 7(1): 1--46, 1970.

6. Weyl, H. "Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen." *Mathematische Annalen*, 71: 441--479, 1912.

7. von Neumann, J. "Charakterisierung des Spektrums eines Integraloperators." *Actualites Scientifiques et Industrielles*, 229, Hermann, Paris, 1935.

8. Wilkinson, J.H. *The Algebraic Eigenvalue Problem*. Oxford University Press, 1965.

9. Reed, M. & Simon, B. *Methods of Modern Mathematical Physics*, Vol. I--IV. Academic Press, 1972--1978.

10. Bhatia, R. *Matrix Analysis*. Graduate Texts in Mathematics 169, Springer-Verlag, New York, 1997.

11. Simon, B. "Tosio Kato's Work on Non-Relativistic Quantum Mechanics: Part 1." *Bulletin of Mathematical Sciences*, 8(1): 121--232, 2018.

12. Yafaev, D.R. *Mathematical Scattering Theory: Analytic Theory*. Mathematical Surveys and Monographs, Vol. 158, American Mathematical Society, 2010.

---

*本文完成于2026年4月。*

Sources:
- [Perturbation Theory for Linear Operators - Springer](https://link.springer.com/book/10.1007/978-3-642-66282-9)
- [Tosio Kato - Wikipedia](https://en.wikipedia.org/wiki/Tosio_Kato)
- [Tosio Kato's work on non-relativistic quantum mechanics: part 1 - Simon](https://link.springer.com/article/10.1007/s13373-018-0118-0)
- [Kato 1951 paper - AMS](https://www.ams.org/journals/tran/1951-070-02/S0002-9947-1951-0041010-X/S0002-9947-1951-0041010-X.pdf)
- [Davis-Kahan sin theta theorem notes](https://www.cs.columbia.edu/~djhsu/coms4772-f16/lectures/davis-kahan.pdf)
- [Perturbation theory of polynomials and linear operators](https://arxiv.org/html/2308.01299)
- [Kato-Rellich Theorem - Bohrium](https://www.bohrium.com/en/sciencepedia/feynman/keyword/kato_rellich_theorem)
- [Perturbation Theory for Linear Operators - Full PDF](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/kato1.pdf)
- [SciSpace citation data](https://scispace.com/papers/perturbation-theory-for-linear-operators-3otm06li8i)
- [AMS Wiener Prize history](https://mathshistory.st-andrews.ac.uk/Honours/AMSWienerPrize/)
